### RPM external vecgeom v1.1.20
## INCLUDE compilation_flags
%define tag ccc45b15420e60f39b60107795a85fed12332005
Source: git+https://gitlab.cern.ch/VecGeom/VecGeom.git?obj=master/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
BuildRequires: cmake gmake
%define keep_archives true
%define vecgeom_backend Scalar
Patch0: vecgeom-fix-vector

%prep
%setup -n %{n}-%{realversion}

%patch0 -p1

%build
rm -rf ../build
mkdir ../build
cd ../build

cmake ../%{n}-%{realversion} \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DROOT=OFF \
  -DCMAKE_BUILD_TYPE=Release \
  -DNO_SPECIALIZATION=ON \
  -DBUILTIN_VECCORE=ON \
  -DBACKEND=%{vecgeom_backend} \
%ifarch x86_64
%if "%{vecgeom_backend}" == "Vc"
  -DVECGEOM_VECTOR=sse3 \
%endif
%endif
  -DCMAKE_VERBOSE_MAKEFILE=TRUE \
  -DCMAKE_CXX_STANDARD=17 \
%if "%{?arch_build_flags}"
  -DCMAKE_CXX_FLAGS="%{arch_build_flags}" \
%endif
  -DGEANT4=OFF \
  -DDATA_DOWNLOAD=OFF

make %{makeprocesses}

%install
cd ../build
make %{makeprocesses} install

%post
%{relocateConfig}lib/cmake/VecGeom/*.cmake
