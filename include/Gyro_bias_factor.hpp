#include <ceres/ceres.h>
#include <Eigen/Core>
#include <Eigen/Dense>
struct GyroScopeBiasEdgeFactor
{
    GyroScopeBiasEdgeFactor() {}
    GyroScopeBiasEdgeFactor(const Eigen::Matrix3d & xxF, const Eigen::Matrix3d & yyF, const Eigen::Matrix3d & zzF, const Eigen::Matrix3d & xyF, const Eigen::Matrix3d & yzF, const Eigen::Matrix3d& zxF, Eigen::Matrix3d dR_dbg, Eigen::Matrix3d R_ij, Eigen::Matrix3d ric): 
    mxxF(xxF), myyF(yyF), mzzF(zzF), mxyF(xyF), myzF(yzF), mzxF(zxF), mdR_dbg(dR_dbg), mR_ij(R_ij), mRbc(ric){}


    template<typename T>
    bool operator()(const T *bg, T *residual) const 
    {
        // Cast type
        Eigen::Matrix<T,3,3> Rbc = mRbc.cast<T>();
        Eigen::Matrix<T,3,3> Rij = mR_ij.cast<T>();
        Eigen::Matrix<T,3,3> dR_dbg = mdR_dbg.cast<T>();
        Eigen::Matrix<T,3,1> est_bg{bg[0], bg[1], bg[2]};

        Eigen::Matrix<T,3,1> jbg = dR_dbg * est_bg;
        Eigen::Matrix<T,3,1> halfangle = jbg / static_cast<T>(2.0);
        Eigen::Quaternion<T> delta_Q (static_cast<T>(1.0), halfangle.x(), halfangle.y(), halfangle.z());
        Eigen::Matrix<T,3,3> Rij_update = Rij * (delta_Q.normalized().toRotationMatrix());
        // Compose M
        Eigen::Matrix<T,3,3> M;
        Eigen::Matrix<T,3,3> R = Rbc.transpose() * Rij_update * Rbc;
        T temp;
        temp = R.row(2)*myyF*R.row(2).transpose();
        M(0,0)  = temp;
        temp = static_cast<T>(-2.0)*R.row(2)*myzF*R.row(1).transpose();
        M(0,0) += temp;
        temp = R.row(1)*mzzF*R.row(1).transpose();
        M(0,0) += temp;

        temp =  R.row(2)*myzF*R.row(0).transpose();
        M(0,1)  = temp;
        temp = static_cast<T>(-1.0)*R.row(2)*mxyF*R.row(2).transpose();
        M(0,1) += temp;
        temp = static_cast<T>(-1.0)*R.row(1)*mzzF*R.row(0).transpose();
        M(0,1) += temp;
        temp =  R.row(1)*mzxF*R.row(2).transpose();
        M(0,1) += temp;

        temp =  R.row(2)*mxyF*R.row(1).transpose();
        M(0,2)  = temp;
        temp = static_cast<T>(-1.0)*R.row(2)*myyF*R.row(0).transpose();
        M(0,2) += temp;
        temp = static_cast<T>(-1.0)*R.row(1)*mzxF*R.row(1).transpose();
        M(0,2) += temp;
        temp = R.row(1)*myzF*R.row(0).transpose();
        M(0,2) += temp;

        temp = R.row(0)*mzzF*R.row(0).transpose();
        M(1,1) = temp;
        temp = static_cast<T>(-2.0)*R.row(0)*mzxF*R.row(2).transpose();
        M(1,1) += temp;
        temp = R.row(2)*mxxF*R.row(2).transpose();
        M(1,1) += temp;

        temp =  R.row(0)*mzxF*R.row(1).transpose();
        M(1,2) = temp;
        temp = static_cast<T>(-1.0)*R.row(0)*myzF*R.row(0).transpose();
        M(1,2) += temp;
        temp = static_cast<T>(-1.0)*R.row(2)*mxxF*R.row(1).transpose();
        M(1,2) += temp;
        temp = R.row(2)*mxyF*R.row(0).transpose();
        M(1,2) += temp;

        temp = R.row(1)*mxxF*R.row(1).transpose();
        M(2,2) = temp;
        temp = static_cast<T>(-2.0)*R.row(0)*mxyF*R.row(1).transpose();
        M(2,2) += temp;
        temp = R.row(0)*myyF*R.row(0).transpose();
        M(2,2) += temp;

        M(1,0) = M(0,1);
        M(2,0) = M(0,2);
        M(2,1) = M(1,2);

        //Retrieve the smallest Eigenvalue by the following closed form solution
        T b = -M(0,0)-M(1,1)-M(2,2);
        T c =
            -ceres::pow(M(0,2),2)-ceres::pow(M(1,2),2)-ceres::pow(M(0,1),2)+
            M(0,0)*M(1,1)+M(0,0)*M(2,2)+M(1,1)*M(2,2);
        T d =
            M(1,1)*ceres::pow(M(0,2),2)+M(0,0)*ceres::pow(M(1,2),2)+M(2,2)*ceres::pow(M(0,1),2)-
            M(0,0)*M(1,1)*M(2,2)-static_cast<T>(2)*M(0,1)*M(1,2)*M(0,2);

        T s = static_cast<T>(2)*ceres::pow(b,3)-static_cast<T>(9)*b*c+static_cast<T>(27)*d;
        T t = static_cast<T>(4)*ceres::pow((ceres::pow(b,2)-static_cast<T>(3)*c),3);

        T alpha = ceres::acos(s/ceres::sqrt(t));
        T beta = alpha/static_cast<T>(3);
        T y = ceres::cos(beta);

        T r = static_cast<T>(0.5)*ceres::sqrt(t);
        T w = ceres::pow(r,(1.0/3.0));

        T k = w*y;
        T smallestEV = (-b-static_cast<T>(2)*k)/static_cast<T>(3);

        residual[0] = smallestEV;
      
        return true;
    }


    Eigen::Matrix3d mRbc;
    Eigen::Matrix3d mdR_dbg;
    Eigen::Matrix3d mR_ij;

    Eigen::Matrix3d mxxF, myyF, mzzF, mxyF, myzF, mzxF;
};


