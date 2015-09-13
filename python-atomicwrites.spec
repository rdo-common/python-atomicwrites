# invoke with "--with tests" to enable tests, currently disabled
# as network is required

%bcond_with tests

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:       python-atomicwrites
Version:    0.1.8
Release:    1%{?git_tag}%{?dist}
Summary:    Python Atomic file writes on POSIX 

License:    MIT
URL:        https://github.com/untitaker/%{name}
Source0:    https://github.com/untitaker/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:  noarch

BuildRequires:  python-devel
%global short_name atomicwrites

BuildRequires:  python-setuptools
BuildRequires:  python-sphinx
BuildRequires:  python-tox
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-sphinx
# No python3-tox exists yet
%endif


%description
This Python module provides atomic file writes on POSIX operating systems.
It sports:
* Race-free assertion that the target file doesn't yet exist
* Windows support
* Simple high-level API that wraps a very flexible class-based API

%if %{with python3}
%package -n python3-%{short_name}
Summary:    Python Atomic file writes on POSIX 

%description -n python3-%{short_name}
This Python module provides atomic file writes on POSIX operating systems.
It sports:
* Race-free assertion that the target file doesn't yet exist
* Windows support
* Simple high-level API that wraps a very flexible class-based API
%endif

%prep
%setup -q

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py --quiet build
export PYTHONPATH=`pwd`
cd docs
make %{?_smp_mflags} man
cd ..
unset PYTHONPATH

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py --quiet build
export PYTHONPATH=`pwd`
cd docs
make %{?_smp_mflags} SPHINXBUILD=sphinx-build-3 man
cd ..
unset PYTHONPATH
popd
%endif


%install
%{__python} setup.py --quiet install -O1 --skip-build --root $RPM_BUILD_ROOT
install -d "$RPM_BUILD_ROOT%{_mandir}/man1"
cp -r docs/_build/man/*.1 "$RPM_BUILD_ROOT%{_mandir}/man1"

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root $RPM_BUILD_ROOT
popd
%endif

%check
%if %{with tests}
%{__python} run-tests.py
%endif

# needs python3-tox bz #1010767
#if {with python3}
#{__python3} run-tests.py
#endif

%files
%doc LICENSE README.rst
%{python_sitelib}/*
%{_mandir}/man1/atomicwrites.1.*

%if %{with python3}
%files -n python3-%{short_name}
%doc README.rst LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Sun Sep 13 2015 Michele Baldessari <michele@acksyn.org> - 0.1.8-1
- New upstream (BZ 1262584)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 08 2015 Michele Baldessari <michele@acksyn.org> - 0.1.5-1
- New upstream (BZ 1209294)

* Mon Mar 02 2015 Michele Baldessari <michele@redhat.com> - 0.1.4-5
- Disable tests as they require network

* Sun Mar 01 2015 Michele Baldessari <michele@redhat.com> - 0.1.4-4
- Move it to python 3

* Sat Feb 28 2015 Michele Baldessari <michele@redhat.com> - 0.1.4-3
- Fix check section and add python-tox as BR

* Sat Feb 28 2015 Michele Baldessari <michele@redhat.com> - 0.1.4-2
- Improve description

* Mon Feb 23 2015 Michele Baldessari <michele@redhat.com> - 0.1.4-1
- New upstream

* Wed Feb 04 2015 Michele Baldessari <michele@redhat.com> - 0.1.1-3
- Add python-sphinx BR

* Wed Oct 01 2014 Michele Baldessari <michele@redhat.com> - 0.1.1-1
- Initial packaging
