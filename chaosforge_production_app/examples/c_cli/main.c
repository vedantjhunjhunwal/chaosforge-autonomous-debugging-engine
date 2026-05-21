#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int extract_price(const char* s) {
    const char* p = strstr(s, "price");
    if (!p) return 1;
    while (*p && (*p < '0' || *p > '9')) p++;
    return atoi(p);
}

int main(int argc, char** argv) {
    const char* payload = argc > 1 ? argv[1] : "{}";
    int amount = 100;
    int price = extract_price(payload);
    int result = amount / price;
    printf("%d\n", result);
    return 0;
}
