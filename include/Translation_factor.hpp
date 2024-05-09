#include <ceres/ceres.h>
#include <Eigen/Core>
#include <Eigen/Dense>
struct TranslationFactor
{
    TranslationFactor(double nx, double ny, double nz): 
    _nx(nx), _ny(ny), _nz(nz) {}


    template<typename T>
    bool operator()(const T *t, T *residual) const 
    {
        residual[0] = - (t[0] * T(_nx) + t[1] * T(_ny) + t[2] * T(_nz));
        return true;
    }


   const double _nx, _ny, _nz;
};

