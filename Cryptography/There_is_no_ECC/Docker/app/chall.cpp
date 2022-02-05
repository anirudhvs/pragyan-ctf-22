#include <iostream>
#include <gmp.h>
#include <random>
#include <fstream>
using namespace std;
class Challenge
{
private:
    std::string flag;
    mpz_t pt, s, ord, X, r;
    void gen_rand_prime(mpz_t &, const uint32_t);
    void gen_rand_range(mpz_t &, const mpz_t &);

public:
    Challenge(std::string);
    ~Challenge();
    void run();
};

Challenge::Challenge(string flag)
{
    mpz_init(this->pt);
    mpz_init(this->s);
    mpz_init(this->ord);
    mpz_init(this->X);
    mpz_init(this->r);
    this->flag = flag;
    gen_rand_prime(this->ord, 512);
    gen_rand_range(this->r, this->ord);
    gen_rand_range(this->X, this->ord);
    const uint32_t BUFFER_SIZE = this->flag.length();
    uint8_t buf[BUFFER_SIZE];

    for (uint32_t i = 0; i < BUFFER_SIZE; i++)
        buf[i] = this->flag.at(i);

    mpz_init(this->pt);
    mpz_import(this->pt, BUFFER_SIZE, 1, sizeof(buf[0]), 0, 0, buf);
}

Challenge::~Challenge()
{
    mpz_clears(pt, s, ord, X, r, NULL);
}

void Challenge::gen_rand_prime(mpz_t &prime, const uint32_t nbits) //getPrime(nbits)
{
    const uint8_t rem = nbits % 8;
    const uint32_t BUFFER_SIZE = (nbits >> 3) + bool(rem);
    uint8_t buf[BUFFER_SIZE];

    std::random_device rand;

    do
    {
        for (uint32_t i = 0; i < BUFFER_SIZE; i++)
            buf[i] = rand() % (1 << 8);

        if (rem == 0)
            buf[BUFFER_SIZE - 1] |= 1 << 7;
        else
        {
            buf[BUFFER_SIZE - 1] &= (1 << rem) - 1;
            buf[BUFFER_SIZE - 1] |= 1 << (rem - 1);
        }

        buf[0] |= 0x01;

        mpz_t temp;
        mpz_init(temp);
        mpz_import(temp, BUFFER_SIZE, 1, sizeof(buf[0]), 0, 0, buf);
        mpz_nextprime(prime, temp);
        mpz_clear(temp);
    } while (mpz_sizeinbase(prime, 2) != nbits);
}

void Challenge::gen_rand_range(mpz_t &random, const mpz_t &src) //randint(1,random-1)
{
    std::random_device rand;
    gmp_randstate_t state;
    gmp_randinit_mt(state);
    gmp_randseed_ui(state, rand());
    mpz_urandomm(random, state, src);
    if (mpz_cmp_ui(random, 0) == 0)
        mpz_set_ui(random, 69420);
}

void Challenge::run()
{
    int thing, i = 0;
    mpz_t temp1, temp2;
    mpz_init(temp1);
    mpz_init(temp2);
    string store;
    store = mpz_get_str(NULL, 10, ord);
    cout << "Order of point G is: " << store << "\n";
    for (i; i < 2; i++)
    {
        cout << "Enter:";
        cin >> thing;
        mpz_set_ui(s, thing);
        mpz_mul(temp1, r, s);
        mpz_mul(temp1, temp1, X);
        mpz_mod(temp1, temp1, ord);
        mpz_powm(temp1, temp1, s, ord);
        mpz_mul(temp2, pt, s);
        mpz_mod(temp2, temp2, ord);
        mpz_mul(temp2, temp2, temp1);
        store = mpz_get_str(NULL, 10, temp2);
        cout << "You received " << store << "\n";
    }
    mpz_clear(temp1);
    mpz_clear(temp2);
}

int main()
{
    std::ifstream fin("flag.txt");
    std::string flag;
    std::getline(fin, flag);
    flag.erase(flag.find_last_not_of(" \n\t\r") + 1);
    fin.close();
    Challenge chall(flag);
    chall.run();
    return 0;
}
