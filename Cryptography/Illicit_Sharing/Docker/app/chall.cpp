#include <iostream>
#include <gmp.h>
#include <random>
#include <fstream>

class RSAKey
{
    private:
        void gen_rand_prime(mpz_t&, const uint32_t);

    public:
        mpz_t p;
        mpz_t q;
        mpz_t n;

        RSAKey(void);
        ~RSAKey();
        void gen_rand_key(const uint32_t, const uint32_t);
};

class Challenge
{
    private:
        std::string flag;
        mpz_t pt;

        uint32_t p_nbits;
        uint32_t q_nbits;
        uint32_t shared_nbits;

        void generate_insecure_keys(RSAKey&, RSAKey&);
        void gen_rand_bits(mpz_t&, const uint32_t);
        void encrypt_flag(mpz_t&, const RSAKey&, const mpz_t&);
        std::string gen_output(void);
    
    public:
        Challenge(std::string, const uint32_t, const uint32_t, const uint32_t);
        ~Challenge();
        void run(void);
};

RSAKey::RSAKey(void)
{
    mpz_init(this->p);
    mpz_init(this->q);
    mpz_init(this->n);
}

RSAKey::~RSAKey()
{
    mpz_clear(this->p);
    mpz_clear(this->q);
    mpz_clear(this->n);
}

void RSAKey::gen_rand_prime(mpz_t &prime, const uint32_t nbits)
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

        mpz_t temp; mpz_init(temp);
        mpz_import(temp, BUFFER_SIZE, 1, sizeof(buf[0]), 0, 0, buf);
        
        mpz_nextprime(prime, temp);
        mpz_clear(temp);
    }
    while (mpz_sizeinbase(prime, 2) != nbits);
}

void RSAKey::gen_rand_key(const uint32_t ps, const uint32_t qs)
{
    this->gen_rand_prime(this->p, ps);
    this->gen_rand_prime(this->q, qs);

    mpz_mul(this->n, this->p, this->q);
}

Challenge::Challenge(const std::string str, const uint32_t ps, const uint32_t qs, const uint32_t sb)
{
    this->flag = str;
    this->p_nbits = ps;
    this->q_nbits = qs;
    this->shared_nbits = sb;

    const uint32_t BUFFER_SIZE = this->flag.length();
    uint8_t buf[BUFFER_SIZE];

    for (uint32_t i = 0; i < BUFFER_SIZE; i++)
        buf[i] = this->flag.at(i);
    
    mpz_init(this->pt);
    mpz_import(this->pt, BUFFER_SIZE, 1, sizeof(buf[0]), 0, 0, buf);
}

Challenge::~Challenge()
{
    mpz_clear(this->pt);
}

void Challenge::generate_insecure_keys(RSAKey &key0, RSAKey &key1)
{
    mpz_t xor_; mpz_init(xor_);
    mpz_t cmp; mpz_init(cmp);
    mpz_ui_pow_ui(cmp, 2, this->shared_nbits);
    
    while (true)
    {
        key0.gen_rand_key(this->p_nbits, this->q_nbits);

        mpz_nextprime(key1.p, key0.p);
        mpz_nextprime(key1.q, key0.q);
        mpz_mul(key1.n, key1.p, key1.q);

        if (mpz_sizeinbase(key0.p, 2) != mpz_sizeinbase(key1.p, 2))
            continue;
        
        mpz_xor(xor_, key0.p, key1.p);
        
        if (mpz_cmp(xor_, cmp) >= 0)
            continue;

        else if (mpz_sizeinbase(key0.q, 2) != mpz_sizeinbase(key1.q, 2))
            continue;
        
        else if (mpz_sizeinbase(key0.n, 2) != mpz_sizeinbase(key1.n, 2))
            continue;
        
        break;
    }
}

void Challenge::gen_rand_bits(mpz_t &random, const uint32_t nbits)
{
    std::random_device rand;
    gmp_randstate_t state;

    gmp_randinit_mt (state);
    gmp_randseed_ui(state, rand());

    mpz_urandomb(random, state, nbits);
}

void Challenge::encrypt_flag(mpz_t &ct, const RSAKey &key, const mpz_t &rand)
{
    mpz_t noise; mpz_init(noise);
    mpz_t phi_q; mpz_init(phi_q);

    mpz_powm(ct, this->pt, key.p, key.n);
    mpz_sub_ui(phi_q, key.q, 1);
    mpz_powm(noise, rand, phi_q, key.n);
    mpz_add(ct, ct, noise);
    mpz_mod(ct, ct, key.n);
}

std::string Challenge::gen_output(void)
{
    RSAKey key0, key1;
    this->generate_insecure_keys(key0, key1);

    mpz_t rand0; mpz_init(rand0);
    mpz_t rand1; mpz_init(rand1);
    this->gen_rand_bits(rand0, this->shared_nbits);
    this->gen_rand_bits(rand1, this->shared_nbits);

    mpz_t ct0; mpz_init(ct0);
    mpz_t ct1; mpz_init(ct1);
    this->encrypt_flag(ct0, key0, rand0);
    this->encrypt_flag(ct1, key1, rand1);

    std::string output;
    output += std::string("n0 = ") + mpz_get_str(nullptr, 10, key0.n) + std::string("\n");
    output += std::string("n1 = ") + mpz_get_str(nullptr, 10, key1.n) + std::string("\n");
    output += std::string("ct0 = ") + mpz_get_str(nullptr, 10, ct0) + std::string("\n");
    output += std::string("ct1 = ") + mpz_get_str(nullptr, 10, ct1) + std::string("\n");

    return output;
}

void Challenge::run(void)
{
    std::string input;
    std::string valid("E");

    while (true)
    {
        std::cout << "Press " << valid << " to encrypt: ";
        std::getline(std::cin, input);

        if (input.compare(valid))
            break;
        else
            std::cout << this->gen_output() << std::endl;
    }
}

int main(int argc, char *argv[])
{
    std::ifstream fin("flag.txt");

    std::string flag;
    std::getline(fin, flag);
    flag.erase(flag.find_last_not_of(" \n\t\r") + 1);
    
    fin.close();

    Challenge chall(flag, 1024, 255, 512);
    chall.run();

    return 0;
}
