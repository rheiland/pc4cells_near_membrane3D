// https://mathworld.wolfram.com/Point-LineDistance3-Dimensional.html
#include <iostream>
#include <vector>
#include <numeric>
#include <algorithm> 
#include <cmath> 

int main()
{
    // compute closest distance on a line segment, x1-x2, from a point, x0 (in 3D)
    //  tval = - ((x1 - x0) dot (x2 - x1)) / |x2 - x1|^2
    // point
    std::vector<double> x0{50., -42., 100.};

    // line segment (axis of cylinder)
    std::vector<double> x1{0., -400., 300.};
    std::vector<double> x2{0., 400., 300.};
    std::cout << "x0 = ";
    for (auto v: x0) std::cout << v << ' '; std::cout << std::endl;
    std::cout << "x1 = ";
    for (auto v: x1) std::cout << v << ' '; std::cout << std::endl;
    std::cout << "x2 = ";
    for (auto v: x2) std::cout << v << ' '; std::cout << std::endl;

    std::vector<double> x1m0 = x1;
    std::transform(x1.begin(),x1.end(), x0.begin(),x1m0.begin(), std::minus<double>());
    std::cout << "x1m0: " << std::endl;
    for (auto v: x1m0) std::cout << v << ' '; std::cout << std::endl;

    std::vector<double> x2m1 = x1;
    std::transform(x2.begin(),x2.end(), x1.begin(),x2m1.begin(), std::minus<double>());
    std::cout << "x2m1: " << std::endl;
    for (auto v: x2m1) std::cout << v << ' '; std::cout << std::endl;


    //  t = - ((x1 - x0) dot (x2 - x1)) / |x2 - x1|^2

    double numer = std::inner_product(x1m0.begin(), x1m0.end(), x2m1.begin(), 0);
    double xv = x2m1[0];
    double yv = x2m1[1];
    double zv = x2m1[2];
    double denom = xv*xv + yv*yv + zv*zv;
    double tval = -numer / denom;
    std::cout << "tval= " << tval << std::endl;

    double xp = x1[0] + tval * (x2[0] - x1[0]);
    double yp = x1[1] + tval * (x2[1] - x1[1]);
    double zp = x1[2] + tval * (x2[2] - x1[2]);
    std::cout << "xp: pt on line seg = " << xp << ", " << yp << ", " << zp << std::endl;

    std::vector<double> xpv={x0[0]-xp, x0[1]-yp, x0[2]-zp};
    std::cout << "xpv: xp -> x0 = " << xpv[0] << ", " << xpv[1] << ", " << xpv[2] << std::endl;

    double xpvdist = std::sqrt(xpv[0]*xpv[0] + xpv[1]*xpv[1] + xpv[2]*xpv[2]); 
    std::cout << "dist(xp-x0) = " << xpvdist << std::endl;

    std::vector<double> xpvu={xpv[0]/xpvdist, xpv[1]/xpvdist, xpv[2]/xpvdist};
    std::cout << "xpvu: unit vec xp -> x0 = " << xpvu[0] << ", " << xpvu[1] << ", " << xpvu[2] << std::endl;

    double R_cyl = 400.0;
    std::vector<double> xpcyl={xpvu[0]*R_cyl, xpvu[1]*R_cyl, xpvu[2]*R_cyl};
    std::cout << "xpcyl = " << xpcyl[0] << ", " << xpcyl[1] << ", " << xpcyl[2] << std::endl;

    // std::cout << "normalized = " << xp << ", " << yp << ", " << zp << std::endl;
    
    // std::cout << "x1 = " << x1 << '\n';
    // std::cout << "x2 = " << x2 << '\n';

    // std::cout << "x1 - x0 = " << tval << '\n';

    // double r1 = std::inner_product(;
    // std::cout << "tval = " << tval << '\n';
    // // double r1 = std::inner_product(a.begin(), a.end(), b.begin(), 0);
    // std::cout << "Inner product of a and b: " << r1 << '\n';
}
