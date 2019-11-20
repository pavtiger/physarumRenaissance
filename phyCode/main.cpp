#include <bits/stdc++.h>
using namespace std;

const int h = 500;
const int w = 500;
const int l = 500;
const GLuint lengh = 10;

/*
int SIZE = [600, 500, 400];
int SENSORS = False;
int FOOD_EAT = 40;
int FOOD = True;
int SIZE = (600, 600);
int CL = (33, 33, 33);
*/


class modeling { // ответственнен за обработку данных  и их выывод
public:
    vector<int>

    void draw_output() {
        // code
    }

    void make_circle() {
        // code
    }

    void location_update() {
        // code
    }
};


class particle { // частица
public: // параметры
    GLint SA = 45;
    GLint RA = 20;
    int SO = 9
    int SS = 0.5;
    int depT = 5;
    int pCD = 0;
    int sMin = 0;
    int food = 255;
    int foodTrH = 20;
    int x = x;
    int y = y;
    int heading = heading;


    void p_share() { // поделиться едой с соседями
        // code
    }


    void p_test() { //
        // code
    }


    void p_move() { // подвинуться на SS по angle
        // code
    }


    void p_rotate(int ans) { // повернуться
        if (ans[0][1] > 0 or ans[2][1] > 0) {
            if (ans[0][1] > ans[2][1]) {
                // turn left
                heading += 5;
            } else {
                // turn right
                heading -= 5;
            }
        }
    }


    void p_sense() { // собрать данные с сенсоров
        // code
    }
};



int main() {
    int TrailMap[l][w] // след, препятствия
    inе FoodMap[l][w] // еда

    while (!done) {
        // read mouse
        for (int y = 0; y < l; ++y) {
            for (int x = 0; x <= w; ++x) {
                int value = FoodMap[z][y][x];
                if (value > 0) {
                    // draw green
                } else if (value < 0) {
                    // draw red
                }
            }
        }
        
        for (int p = 0; p < lengh; ++p) {
            model.arr
        }
    }
}
