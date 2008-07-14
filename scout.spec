#
# spec file for package scout
#

# norootforbuild

Name:           scout
Version:        0.0.2
Release:        1
Url:            http://en.opensuse.org/Scout
License:        MIT License
Group:          System/Packages
Summary:        Package Scout
Source:         %{name}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
BuildRequires:  python rpm-python
Requires:       python

%if 0%{?suse_version}
BuildRequires:  python-xml
%endif

%if 0%{?fedora_version} || 0%{?rhel_version} || 0%{?centos_version}
%define py_sitedir %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")
%endif

# workaround conflicting readline packages
%if 0%{?suse_version} <= 1020
BuildRequires:  readline
%endif

%description

Package Scout for indexing various properties of packages.

%package -n command-not-found
Version:        0.1.0
Release:        1
License:        MIT License
Group:          System/Shells
Summary:        Command Not Found extension for shell
Requires:       python rpm-python
Requires:       bash(CommandNotFound)
%define distro error
%if 0%{?suse_version} > 1030
%define distro suse110
%endif
%if 0%{?suse_version} <= 1030 && 0%{?suse_version} > 1020
%define distro suse103
%endif
%if 0%{?suse_version} <= 1020 && 0%{?suse_version} > 1010
%define distro suse102
%endif
%if 0%{?suse_version} <= 1010 && 0%{?suse_version} > 1000
%define distro suse101
%endif
Requires:       scout scout-bin-%{distro}

%description -n command-not-found
The "command not found" message is not very helpful. If e.g. the unzip command
is not found but it's available in a package, it would be very interesting
if the system could tell that the command is currently not available,
but installing a package would provide it.

%prep
%setup -q -n %{name}

%build
# compile scripts
python -mcompileall .

%install
# --- scout ---
# install python scripts
mkdir -p $RPM_BUILD_ROOT%{py_sitedir}/%{name}
shopt -s extglob
cp -a scout/!(foo).py{,c} $RPM_BUILD_ROOT%{py_sitedir}/%{name}
# install data files
install -D -m 0644 repos.conf $RPM_BUILD_ROOT%{_datadir}/%{name}/repos.conf
# install scout binary
install -D -m 0755 scout-cmd.py $RPM_BUILD_ROOT%{_bindir}/%{name}
# install bash completion
install -D -m 0644 scout-bash-completion $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/scout
# install manpage
install -D -m 0644 doc/scout.1 $RPM_BUILD_ROOT%{_mandir}/man1/scout.1

# --- command-not-found ---
install -D -m 755 handlers/bin/command-not-found $RPM_BUILD_ROOT%{_bindir}/command-not-found
for shell in bash zsh; do
    install -D -m 644 handlers/bin/command_not_found_${shell} $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
    sed -i 's:__DISTRO__:%{distro}:' $RPM_BUILD_ROOT%{_sysconfdir}/${shell}_command_not_found
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS LICENSE README TODO doc/scout.html doc/scout.pdf
%{_bindir}/%{name}*
%{py_sitedir}/%{name}
%{_datadir}/%{name}
%{_sysconfdir}/bash_completion.d/*
%{_mandir}/man1/*

%files -n command-not-found
%defattr(-,root,root)
%doc handlers/bin/README
%{_bindir}/command-not-found
%{_sysconfdir}/*_command_not_found

%changelog
