%define modname mcache
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A39_%{modname}.ini

Summary:	A PHP extension providing access to memcached caching servers
Name:		php-%{modname}
Version:	1.2.0
Release:	%mkrel 0.beta10.11
Group:		Development/PHP
License:	PHP License
URL:		http://www.klir.com/~johnm/php-mcache/
Source0:	http://www.klir.com/~johnm/php-mcache/php-%{modname}-ext-%{version}-beta10.tar.bz2
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	libmemcache-devel >= 1.4.0
Epoch:		2
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
mcache is a PHP extension that aims to enable developers to easily and
efficiently cache data to Memcached servers. Memcached is a distributed data
caching system developed by Danga which aims to reduce load on central
bottlenecks like RDBMS's. The mcache php extension has been developed by John
McCaskey and is a wrapper around libmemcache. Both Sean Chittenden (author of
libmemcache), and Antony Dovgal (author of the original PECL memcached
extensions) deserve some of the credit for this work. Without the excellent C
API of libmemcache I would have never written this extension, and likewise
without the example of the PECL extension provided by Antony I would likely
have taken much longer to learn how to write a PHP extension properly. 

The primary advantage to using this mcache extension over other PHP extensions
is speed, and functionality. Previously several PHP memcache API's have
existed. Several of these are very good feature-wise, but very slow due to
native PHP implementation. The PECL extension has excellent speed (although not
as good as  mcache), but does not support multiple servers. Users have been
forced to choose between speed and functionality. With the introduction of this
new extension that is no longer the case. Furthermore, because this extension
is based off libmemcache it will easily benefit from any testing, bug fixes, or
enhancements made to the underlying library. 

%prep

%setup -q -n php-%{modname}-ext-%{version}-beta10

%build
%serverbuild

#%{_usrsrc}/php-devel/buildext mcache "mcache.c" \
#    "-lmemcache" "-DCOMPILE_DL_MCACHE"

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}
[ "../package.xml" != "/" ] && rm -f ../package.xml

%files 
%defattr(-,root,root)
%doc README* CREDITS index.html mcache.php
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
