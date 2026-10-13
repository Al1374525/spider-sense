#include <iostream>
const int CAPACITY = 64;
const unsigned char SYNC_BYTE = 0xAA;

enum DecodeStat{
    syncNotFound,
    incomplete,
    ready,
    badLength

};


struct RingBuffer{

    unsigned char buffer[CAPACITY];
    int head;
    int tail;
    int count;
};

void init(RingBuffer* rb){
    rb->head = 0;
    rb->tail =0;
    rb->count = 0;
}

bool push(RingBuffer* rb,unsigned char byte){
    if(rb->count == CAPACITY){
        return false;
    }

   rb->buffer[rb->head] = byte; //store byte at head
    rb->head = (rb->head + 1 ) % CAPACITY; // Advance head, wrapping at CAPACITY
    rb->count++; // Increment count

    return true;
}

bool pop(RingBuffer* rb,  unsigned char* out){
    if(rb->count ==0){
        return false;
    }

    //2. Get the byte at tail
    *out = rb->buffer[rb->tail];

    //3. Advance tail, wrapping around the buffer capacity
    rb->tail = (rb->tail + 1) % CAPACITY;

    //4. Decrement count
    
    rb->count--;

    return true;

}

bool peek(RingBuffer* rb, int offset, unsigned char* out){
    if( offset < 0 ||offset >= rb->count){
        return false;
    }

    int slot = (rb->tail + offset) % CAPACITY;
    *out = rb->buffer[slot];

    return true;
}


//Tells the caller whether it found a sync byte
bool find_sync(RingBuffer* rb){
   unsigned char byte;
   
   while(peek(rb, 0, &byte)){
    if(byte== SYNC_BYTE){
        return true;
    }
    pop(rb, &byte);

   }
   return false;
}

DecodeStat check_packet(RingBuffer* rb){

    if(find_sync(rb) == false ){
        return syncNotFound;

    }

    unsigned char length;
    if(!peek(rb, 1, &length)){

        return incomplete;

    }

    int packet_size = length + 3;

    if (packet_size > CAPACITY){
        pop(rb, &length);
        return badLength;
    }

    if(rb->count < packet_size){
        return incomplete;
    }

    return ready;

}

bool read_packet(RingBuffer* rb, int* out ){
    unsigned char length;
    peek(rb, 1, &length);

    int sum = 0;
    for (int i = 0; i < length; i++){
        unsigned char b;
        peek(rb, 2+ i, &b );

        sum += b;
    }

    //2. read the checksum
    unsigned char checksum;
    peek(rb, 2 + length, &checksum);

    //3 Mismatch: Drop ONE byte (the sync) and leave *out alone
    unsigned char discard;
    if ((sum & 0xFF) != checksum){
        pop(rb, &discard);
        return false;
    }

    // 4. Parse ASCII into hundredths "15.03" -> 1503
    int value = 0;
    int frac_digits = 0;
    bool seen_dot = false;
    bool negative = false;
    bool valid = true;

    for (int i = 0; i < length; i++){
        unsigned char b;
        peek(rb, 2 + i, &b);

        if (b=='-' && i == 0){
            negative = true;
        }
        else if(b == '.' && !seen_dot){
            seen_dot = true;
        }

        else if(b >= '0' && b <= '9'){
            if(!seen_dot){
                value = value * 10 + (b - '0');
            } else if (frac_digits < 2){
                value = value * 10 + (b - '0');
                frac_digits++;
            }
        } else{
            valid  = false;
        }
    }

    while (frac_digits < 2){
        value *= 10;
        frac_digits++;
    }


    // 5. Checksum passed, so the framing is trustworthy: pop the whole packet
    for (int i = 0; i < length + 3; i++){
        pop(rb, &discard);
    }

    if (!valid){
        return false;
    }

    *out = negative ? -value : value;
    return true;

}

int main(){
    RingBuffer rb;
    init(&rb);
    unsigned char value;

    std::cout << "--- basic push/pop --\n";

   
   push(&rb, 10);
   push(&rb, 20);
   push(&rb, 30);
    
    while(pop(&rb, &value)){
        std::cout << (int)value << "\n";
    }

    std::cout << "--- wraparound ---\n";

    for(int i = 0; i < 64;i++){
        push(&rb, (unsigned char)i);
    }

    for (int i =0; i < 32; i++){
        pop(&rb, &value);
    }

    for(int i= 100; i <132; i++){
        push(&rb, (unsigned char)i);
    }

        while (pop(&rb, &value)) {
        std::cout << (int)value << " ";
    }


    std::cout << "\n";

    std::cout << "--- peek ---\n";
    
    //drain anything left over so we can start
    while (pop(&rb, &value)) {}
    push(&rb, 10);
    push(&rb, 20);
    push(&rb, 30);

    std::cout << "before: count=" << rb.count << " tail=" << rb.tail << "\n";

    if (peek(&rb, 2, &value)){
        std::cout << "peek(2) = " << (int)value << "\n";
        std::cout << "after: count=" << rb.count << " tail=" << rb.tail << "\n";

    }

    std::cout << "peek(3) ok?" << peek(&rb, 3, &value) << "\n";
    std::cout << "peek(-1) ok? " << peek(&rb, -1, &value) << "\n";

    std::cout << "--- find_sync ---\n";

    while (pop(&rb, &value)){}

    push(&rb, 1);
    push(&rb, 2);
    push(&rb, 3);
    push(&rb, 0xAA);
    push(&rb, 7);
    push(&rb, 8);

    std::cout << "found? " << find_sync(&rb) << "\n";
    std::cout << "count=" << rb.count << "\n";
    peek(&rb, 0, &value);
    std::cout << "front=" << (int)value << "\n";

    while(pop(&rb, &value)){}

    push(&rb, 1);
    push(&rb, 2);
    push(&rb, 3);

    std::cout <<"found" << find_sync(&rb) << "\n";
    std::cout << "count=" << rb.count << "\n";


    std::cout << "--- check_packet ---\n";
    
    while (pop(&rb, &value)) {}

    push(&rb, 0xAA);
    push(&rb, 5);
    push(&rb, 0x31);
    push(&rb, 0x35);
    DecodeStat s1 = check_packet(&rb);
    std::cout << "partial: " << s1 << " count=" << rb.count << "\n";


    push(&rb, 0x2E);
    push(&rb, 0x30);
    push(&rb, 0x33);
    push(&rb, 0xF7);
    DecodeStat s2 = check_packet(&rb);
    std::cout << "full:   " << s2 << " count= " << rb.count << "\n";

    while (pop(&rb, &value)) {}
    push(&rb, 1);
    push(&rb, 2);
    push(&rb, 3);
    DecodeStat s3 = check_packet(&rb);
    std::cout << "garbage: " << s3 << " count=" << rb.count << "\n";

    while (pop(&rb, &value)) {}
    push(&rb, 0xAA);
    push(&rb, 200);
    push(&rb, 1);
    push(&rb, 2);
    push(&rb, 3);
    DecodeStat s4 = check_packet(&rb);
    std::cout << "Oversized: " << s4 << " count=" << rb.count << "\n";


       std::cout << "--- read_packet ---\n";
    while (pop(&rb, &value)) {}
    int temp = -1;

    // good packet: 15.03
    unsigned char good[] = {0xAA, 0x05, 0x31, 0x35, 0x2E, 0x30, 0x33, 0xF7};
    for (int i = 0; i < 8; i++) push(&rb, good[i]);
    bool ok1 = read_packet(&rb, &temp);
    std::cout << "good: " << ok1 << " temp=" << temp << " count=" << rb.count << "\n";

    // bad checksum (F8 instead of F7)
    temp = -1;
    unsigned char bad[] = {0xAA, 0x05, 0x31, 0x35, 0x2E, 0x30, 0x33, 0xF8};
    for (int i = 0; i < 8; i++) push(&rb, bad[i]);
    bool ok2 = read_packet(&rb, &temp);
    std::cout << "bad:  " << ok2 << " temp=" << temp << " count=" << rb.count << "\n";
    while (pop(&rb, &value)) {}

    // two packets back to back: 15.03 then 9.50
    unsigned char second[] = {0xAA, 0x04, 0x39, 0x2E, 0x35, 0x30, 0xCC};
    for (int i = 0; i < 8; i++) push(&rb, good[i]);
    for (int i = 0; i < 7; i++) push(&rb, second[i]);
    int t1 = -1, t2 = -1;
    bool ok3 = read_packet(&rb, &t1);
    bool ok4 = read_packet(&rb, &t2);
    std::cout << "two:  " << ok3 << " " << t1 << ", " << ok4 << " " << t2
              << " count=" << rb.count << "\n";

}


