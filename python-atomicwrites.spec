# invoke with "--with tests" to enable tests, currently disabled
# as network is required

%bcond_with tests

%if 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:       python-atomicwrites
Version:    1.1.5
Release:    5%{?git_tag}%{?dist}
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


%global _description\
This Python module provides atomic file writes on POSIX operating systems.\
It sports:\
* Race-free assertion that the target file doesn't yet exist\
* Windows support\
* Simple high-level API that wraps a very flexible class-based API

%description %_description

%package -n python2-%{short_name}
Summary: %summary
%{?python_provide:%python_provide python2-%{short_name}}

%description -n python2-%{short_name} %_description

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

%files -n python2-%{short_name}
%doc LICENSE README.rst
%{python_sitelib}/*
%{_mandir}/man1/atomicwrites.1.*

%if %{with python3}
%files -n python3-%{short_name}
%doc README.rst LICENSE
%{python3_sitelib}/*
%endif

%changelog
* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.5-5
- Python 2 binary package renamed to python2-atomicwrites
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.5-2
- Rebuild for Python 3.6

* Sun Sep 04 2016 Michele Baldessari <michele@acksyn.org> - 1.1.5-1
- New upstream release

* Wed Jul 27 2016 Michele Baldessari <michele@acksyn.org> - 1.1.0-1
- New upstream release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sat Mar 26 2016 Michele Baldessari <michele@acksyn.org> - 1.0.0-1
- New upstream release

* Mon Feb 22 2016 Michele Baldessari <michele@acksyn.org> - 0.1.9-1
- New upstream release (BZ 1308379)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

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
