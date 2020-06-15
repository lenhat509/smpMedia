//
//  House.hpp
//  FinalProject
//
//  Created by Kevin Jin on 6/8/20.
//  Copyright © 2020 Kevin Jin. All rights reserved.
//

#ifndef HOUSE_H
#define HOUSE_H

#include <string>
#include <iostream>
#include <iomanip>

class House {
private:
    std::string address;
    long price;
    int beds, baths;
    std::string type;
    int area;
    
public:
    House();
    House(std::string, long, int, int, std::string, int);
    
    void setAddress(std::string a) {
        address = a;
    }
    std::string getAddress() const {
        return address;
    }
    void setPrice(long p) {
        price = p;
    }
    long getPrice() const {
        return price;
    }
    void setBeds(int b) {
        beds = b;
    }
    int getBeds() const {
        return beds;
    }
    void setBaths(int b) {
        baths = b;
    }
    int getBaths() const {
        return baths;
    }
    void setType(std::string t) {
        type = t;
    }
    std::string getType() const {
        return type;
    }
    void setArea(int a) {
        area = a;
    }
    int getArea() const {
        return area;
    }
    
    friend std::ostream& operator << (std::ostream&, const House &right);
};

House::House() {
    address = "";
    price = 0;
    beds = 0;
    baths = 0;
    type = "";
    area = 0;
}

House::House(std::string adrs, long p, int bds, int bths, std::string t, int a) {
    address = adrs;
    price = p;
    beds = bds;
    baths = bths;
    type = t;
    area = a;
}

std::ostream& operator << (std::ostream& out, const House &right) {
        out << std::left
            << std::setw(40) << right.address
            << std::setw(10) << right.price
            << std::setw(5) << right.beds
            << std::setw(5) << right.baths
            << std::setw(20) << right.type
            << std::setw(10) << right.area;
        return out;
}

#endif /* HOUSE_H */
