%define _cross_target m68k-apple-aux
%define gcc_version 2.8.1
%define gcc_release 1
%global __os_install_post %{nil}
# %define _unpackaged_files_terminate_build 0
Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: %{_cross_target}-gcc
Version: %{gcc_version}
Release: %{gcc_release}
Copyright: GPL
Group: Development/Languages
Source0: gcc-%{version}.tar.gz
Source1: libgcc1.a
URL: http://gcc.gnu.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
# BuildRoot: /var/tmp/%{_cross-target}-gcc-root
BuildRequires: binutils >= 2.12.90.0.9-1
BuildRequires: %{_cross_target}-binutils >= 2.14-1
BuildRequires: %{_cross_target}-nonfree >= 3.0.1-1
BuildRequires: zlib-devel
# , gettext, dejagnu
# Make sure pthread.h doesn't contain __thread tokens
BuildRequires: glibc-devel >= 2.2.90-12
Requires: %{_cross_target}-binutils >= 2.14-1
Requires: libgcc >= %{version}-%{release}

%define _gnu %{nil}
%{expand: %%{global} _gcc_is_%{_target_cpu} %%{nil}}
%{?_gcc_is_sparc: %global gcc_target_platform sparc64-%{_vendor}-%{_target_os}}
%{!?_gcc_is_sparc: %global gcc_target_platform %{_target_platform}}

%description
The gcc package contains the GNU Compiler Collection version 2.8.1.
You'll need this package in order to compile C code.

%prep
%setup -q -n gcc-%{version}

%build
rm -fr obj-%{gcc_target_platform}-%{_cross_target}
mkdir obj-%{gcc_target_platform}-%{_cross_target}
cd obj-%{gcc_target_platform}-%{_cross_target}
# cp %{SOURCE1} .
touch libgcc1.a

CC=gcc
OPT_FLAGS=`echo $RPM_OPT_FLAGS|sed -e 's/-fno-rtti//g' -e 's/-fno-exceptions//g'`
CC="$CC" CFLAGS="$OPT_FLAGS" CXXFLAGS="$OPT_FLAGS" XCFLAGS="$OPT_FLAGS" TCFLAGS="$OPT_FLAGS" \
	../configure --target=%{_cross_target} --disable-nls \
	--enable-languages=c --without-headers \
	--with-gnu-as --with-gnu-ld \
	--prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
	--enable-shared --disable-checking
make CLIB= LANGUAGES=c %{?_smp_mflags}

%install
rm -fr $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_infodir}
cd obj-%{gcc_target_platform}-%{_cross_target}
TARGET_PLATFORM=%{gcc_target_platform}-%{_cross_taget}
make CLIB= LANGUAGES=c prefix=$RPM_BUILD_ROOT%{_prefix} mandir=$RPM_BUILD_ROOT%{_mandir}/man1 \
  infodir=$RPM_BUILD_ROOT%{_infodir} install
rm -rf %{buildroot}%{_infodir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README* ChangeLog*
%{_prefix}/bin/*
%{_prefix}/%{_lib}/gcc-lib/%{_cross_target}/%{gcc_version}/*
%{_mandir}/man1/*

%changelog
* Mon Sep 06 2021 Jacob Berkman  <jacob@87k.net> 2.8.1-1
- Inital cross-compiler build for A/UX

* Tue Feb 25 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.2-5
- update from 3_2-rhl8 branch
  - CANNOT_CHANGE_MODE_CLASS to fix various -march=p4 bugs (Vlad Makarov)
  - fix IA-64 glibc miscompilation (Vlad Makarov, Richard Henderson)
  - one more x86-64 fix for the direct %fs TLS access patch
  - limit memory usage of ios_base_storage.cc testcase

* Mon Feb 24 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.2-4
- fix ix86_decompose_address broken by last patch
- never use INDNTPOFF on x86-64

* Mon Feb 24 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.2-3
- update from 3.2 branch
  - PRs other/3782, c/8828, optimization/8613, optimization/9768,
        c/9678, c++/9459
- direct %gs (resp. %fs) TLS access on IA-32 and x86-64 (Richard Henderson)
- don't strip compiler binaries, so that debuginfo is generated for them

* Tue Feb 18 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.2-2
- update from 3.2 branch
  - PRs c/8068, optimization/7702, libstdc++/9169
- fix dwarf2 ICE on s390 (#81428)
- fix denormalized FP constants in hexadecimal notation (#84383)

* Fri Feb 14 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.2-1
- update from 3.2 branch
  - gcc 3.2.2 release
- backport s390{,x} constant pool fixes from trunk
- fix s390{,x} TLS

* Tue Feb 04 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.1-7
- update from 3.2 branch
- alpha TLS support
- on sparc32 make a symlink in %{_prefix}/include/c++/*/
  to make gcc-c++-sparc32 happy
- add %%{build_java} conditionals (Elliot Lee)
- fix ppc64 dynamic linker path

* Sat Feb 01 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.1-6
- add DW_AT_comp_dir attribute to compilation unit even if the
  main input filename is absolute, but at least one of its includes
  are relative

* Tue Jan 28 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.1-5
- update from 3.2 branch
- backport binds_local_p from HEAD
- s390 TLS
- fix -fPIC on ppc32 (#79732)

* Fri Jan 17 2003 Jakub Jelinek  <jakub@redhat.com> 3.2.1-4
- update from 3.2 branch
  - PRs inline-asm/8832, c/8032, other/8947, preprocessor/8880,
    optimization/8599, optimization/8988, c++/8503, c++/8442,
    c++/8031, libstdc++/9269, libstdc++/8707, libstdc++/9151,
    libstdc++/9168, libstdc++/8887
  - skip over DW_CFA_undefined and DW_CFA_same_value argument (#79424,
    PR libstdc++/9076)
- fix IA-64 C++ TLS tests
- x86-64 Java fixes (Andrew Haley)
- change s390x dynamic linker to /lib64/ld64.so.1

* Wed Dec 11 2002 Jakub Jelinek  <jakub@redhat.com> 3.2.1-3
- update from gcc-3_2-rhl8-branch
  - PR other/8882
- don't remove -lpthread from libgcj.spec

* Mon Dec 09 2002 Jakub Jelinek  <jakub@redhat.com> 3.2.1-2
- update from gcc-3_2-rhl8-branch
  - PRs c/7622, preprocessor/8524, libstdc++/8230, libstdc++/8708,
    libstdc++/8790, libstdc++/7445, libstdc++/6745, libstdc++/8399,
    libstdc++/8230
- fix ?: optimization in arguments of possible sibling calls
- never force_const_mem a TLS SYMBOL_REF (Richard Henderson)
- change -pthread so that it adds -lpthread even if -shared
- fix Ada makefile dependency (Rainer Orth)

* Tue Nov 26 2002 Jakub Jelinek  <jakub@redhat.com> 3.2.1-1
- update from gcc-3_2-rhl8-branch
  - gcc 3.2.1 release
  - PRs c/8639, optimization/8275, c/8588, c/8518, c/8439,
	optimization/8599, 
  - fix .eh_frame section in crtend*.o on x86-64
  - make sure .rodata.cstNN section entries have size sh_entsize
  - readonly .eh_frame and .gcc_except_table section (needs
    binutils change too)
  - fix force_to_mode (#77756)
  - avoid creating invalid subregs in combiner (Dale Johannesen,
    #75046, #75415, #76058, #76526, #78406)
  - avoid using strtok in libstdc++-v3 for thread safety
    (Paolo Carlini, Nathan Myers)
- add Ada for s390

* Sun Nov 17 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-14
- really fix check-abi problem on ia64/alpha

* Sat Nov 16 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-13
- update from gcc-3_2-rhl8-branch
  - fix flow (Graham Scott, Jan Hubicka)
  - fix check-abi problem on ia64/alpha (Benjamin Kosnik)
  - fix objc on x86_64 (Jan Hubicka, Nicola Pero)
  - fix x86_64 profiling (Jan Hubicka)
  - better s390* .eh_frame encoding (Ulrich Weigand)
- build ada on x86_64
- add fastjar info and jar and grepjar manual pages

* Tue Nov 12 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-12
- update from gcc-3_2-rhl8-branch
  - PRs c/8467, preprocessor/4890, 8502, c/5351, optimization/7591,
    bootstrap/8146, c/8252, optimization/7520, c/8451, c++/8391,
    target/7856, target/7133, target/6890, middle-end/6994, opt/7944,
    c/761, c++/7788, c++/2521, c++/8160, c++/8149, c++/8287,
    middle-end/6994, c++/7266, c++/7228, c++/8067, c++/7679,
    c++/6579, java/7830, libstdc++/8362, libstdc++/8258, libstdc++/7219,
    libstdc++/8466, libstdc++/8172, libstdc++/8197, libstdc++/8318,
    libstdc++/8348, libstdc++/7961, other/3337, bootstrap/6763,
    bootstrap/8122, libstdc++/8347
  - &&lab1 - &&lab2 doesn't need to be in rw section
  - x86_64 %rip fixes
  - fix jar c without f (#77062)
  - backport all fastjar changes from mainline

* Wed Oct 23 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-11
- update from gcc-3_2-rhl8-branch
  - PRs target/7693, opt/7630, c++/6419, target/7396, c++/8218,
    c++/7676, c++/7584, c++/7478, c++/8134, c++/7524, c++/7176,
    c++/5661, c++/6803, c++/7721, c++/7803, c++/7754, c++/7188,
    libstdc++/8071, libstdc++/8127, c++/6745, libstdc++/8096,
    libstdc++/7811
- fix x86-64 ICE with stdarg in -fpic (#76491)
- fix IA-32 miscompilation of DImode code (Jim Wilson, PR target/6981)

* Wed Oct 16 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-10
- update from gcc-3_2-rhl8-branch
  - PRs target/7370, target/8232, opt/7409, preprocessor/7862,
    preprocessor/8190, optimization/6631, target/5610, optimization/7951,
    target/7723
- allow building even if de_DE locale is not installed (#74503, #75889)
- s390x multilib
- x86-64 TLS fixes
- 15 Java fixes (Anthony Green, Andrew Haley, Tom Tromey,
  PRs java/6005, java/7611, java/8003, java/7950, java/5794, libgcj/7073)
- %%define _unpackaged_files_terminate_build 0
- fix make check-abi

* Fri Oct 11 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-9
- update from gcc-3_2-rhl8-branch
  - __attribute__((tls_model("")))
  - PRs c/7353, opt/7124, opt/7912, opt/7390, doc/7484,
        c/7411, target/8087, optimization/6713
- x86-64 TLS

* Tue Oct  8 2002 Jakub Jelinek  <jakub@redhat.com> 3.2-8
- switch to gcc-3_2-rhl8-branch snapshots
  - thus most of the patches went away as they are in CVS
- merge from gcc-3_2-branch between 20020903 and 20021007
  - PRs target/7434, optimization/6627, preprocessor/8120,
	middle-end/7151, preprocessor/8055, optimization/7335,
	c/7160, target/7842, opt/7515, optimization/7130,
	optimization/6984, c/7150, target/7380, other/7114,
	target/5967, optimization/7120, target/7374, opt/7814,
	c/7102
- backported libffi and libjava bits for x86-64 and s390*
- added sparc* support
- multilib setup for sparc* and x86-64
- some IA-32 TLS fixes (Richard Henderson)

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 3.2-7
- fix calling of C++ destructors in certain cases

* Tue Sep  3 2002 Jakub Jelinek <jakub@redhat.com> 3.2-6
- update from CVS (but revert C++ tail padding patches
  for now)
- further fixes to make libstdc++-v3 build on glibc 2.3
- run libstdc++-v3 make check-abi on IA-32 during testing

* Fri Aug 30 2002 Jakub Jelinek <jakub@redhat.com> 3.2-5
- disable tail copy patches, they seem to still have problems
- make libstdc++-v3 build on glibc 2.3 (and use thread-local
  locale model)
- fix c89 and c99 scripts (#73104)

* Wed Aug 26 2002 Jakub Jelinek <jakub@redhat.com> 3.2-4
- reorder alpha_encode_section_info checks slightly to fix an ICE
  when building glibc and to take better advantage of visibility
  attribute on Alpha
- as gdb is not there yet, disable -momit-leaf-frame-pointer
  by default for now on IA-32
- fix IA-64 bootstrap with tail padding patch (Jason Merrill, Daniel Berlin)
- fix x86-64 %RIP to %rip, only output (%rip) if no other relocation
  is used (Richard Henderson)

* Fri Aug 23 2002 Jakub Jelinek <jakub@redhat.com> 3.2-3
- take advantage of __attribute__((visibility())) on Alpha
- avoid copying tail padding (Jason Merrill)

* Thu Aug 22 2002 Jakub Jelinek <jakub@redhat.com> 3.2-2
- fixed Dwarf2 DW_OP_GNU_push_tls_address patch from Richard Henderson
- don't mention removed -a and -ax options in the documentation
  (Nathan Sidwell, #72233)
- fixed __typeof() followed by __asm() redirection from Alexandre Oliva

* Wed Aug 14 2002 Jakub Jelinek <jakub@redhat.com> 3.2-1
- update to 3.2 release
- fix x86-64 PR target/7559 (Jan Hubicka)
- fix -fprefetch-loop-arrays (Janis Johnson)
- fix x86-64 prefetch (Jan Hubicka)

* Fri Aug  9 2002 Jakub Jelinek <jakub@redhat.com> 3.2-0.3
- istream fix (Benjamin Kosnik)
- emit Dwarf2 DW_OP_GNU_push_tls_address extension for TLS (Richard Henderson)
- temporarily disable __typeof() + __asm() fix

* Thu Aug  8 2002 Jakub Jelinek <jakub@redhat.com> 3.2-0.2
- update from 3.2 branch
  - ABI incompatible changes in libstdc++.so.5, long long bitfield
    layout on IA-32 (both C and C++), oversized bitfields layout
    on IA-32 and bitfields with base type with __attribute__((aligned ()))
  - fix strstream segfaults (#68292, Benjamin Kosnik)
- fix __attribute__((visibility())) together with __asm__()
  function redirection
- fix __typeof() followed by __asm() redirection (Alexandre Oliva)
- fix TLS ICE on glibc (#70061)
- fix K6 ICE on linux kernel (#69989, Richard Sandiford, Jan Hubicka)
- fix inlining bug with labels (#70941)
- fix fold-const bug (#70541)
- fix PR preprocessor/7358 (Neil Booth)
- error when mixing __thread and non-__thread declarations
  (#70059, Aldy Hernandez)
- fix TLS bug on g++.dg/tls/diag-1.C (Jason Merrill)
- add -mcmodel= x86-64 documentation (Andreas Jaeger)
- avoid TLS emitting movl %gs:0, MEMORY on IA-32 (#71033)

* Mon Jul 22 2002 Jakub Jelinek <jakub@redhat.com> 3.2-0.1
- first attempt for gcc 3.2
- remove .la files

* Sat Jul 20 2002 Jakub Jelinek <jakub@redhat.com> 3.1-10
- update from 3.1 branch
  - add throw() to set_new_handler (Andreas Schwab)
  - fixed PR optimization/7147, optimization/7153
- make sure pic register is set up even when the only @PLT calls
  are done in EH basic blocks (Richard Henderson)

* Sun Jul 14 2002 Jakub Jelinek <jakub@redhat.com> 3.1-9
- define %%_gnu to nothing for compatibility

* Sat Jul 13 2002 Jakub Jelinek <jakub@redhat.com> 3.1-8
- update from 3.1 branch
  - fix OpenOffice miscompilation (PR c++/7279, Jason Merrill)
  - PRs c++/7224, c++/6255, optimization/7145, c++/6706, preprocessor/7070,
    middle-end/6963, target/6841, target/6770, target/6719,
    other/6836, libstdc++/7057, libstdc++/7097, libstdc++/3946,
    libstdc++/7173
  - fix a GC bug with named labels in C++ (Jim Wilson)
  - fix ICE on Mesa (Bernd Schmidt, #65771)
- added some NRV tests
- fix typo in i386 specs (PR c/7242)
- fix IA-32 ICE with shifts by negative values followed by compare
  (PR middle-end/7245, #68395)
- fixed DWARF-2 output for const char * (PR debug/7241)
- actually enable __cxa_atexit for standard compliance at configury time
- added PPC as Ada enabled architecture

* Wed Jun 19 2002 Jakub Jelinek <jakub@redhat.com> 3.1-7
- update from 3.1 branch
  - PRs target/6922, opt/6722, c/7030, c/6677, objc/6834, c++/6892,
    c++/6723, opt/6793
- use __cxa_atexit for standard compliance:
  if your C++ project knows it won't call atexit from within its
  static constructors, use -fno-use-cxa-atexit to optimize it
- share hard register rtxs where possible to speed the compiler up (Jeff Law)
- optimize tree_code_* arrays (Kaveh Ghazi)
- don't link prefix.o into libgnat, link libgnat against libgcc_s and
  libgnarl against libgnat
- fix typo in GNAT %%post (#66847, #66941, #66639)
- add TLS support

* Fri Jun  7 2002 Jakub Jelinek <jakub@redhat.com> 3.1-6
- add GNAT
- remove DT_RPATH from Java binaries (#66103)
- obsolete kaffe, install jar as %{_prefix}/bin/jar
- add include/org directory in java
- add rmic and rmiregistry programs to libgcj
- add info documentation for gcj and various man pages
- add message catalogues for da, el, es, fr, ja, nl, sv, tr
- don't put IA-64 vtables with relocations into read-only sections
  with -fpic

* Tue Jun  4 2002 Jakub Jelinek <jakub@redhat.com> 3.1-5
- update from 3.1 branch
  - PRs optimization/6822, preprocessor/6844, target/6838, target/6788,
	libstdc++/6886, libstdc++/6795, libstdc++/6811
- m$ compatibility for unnamed fields as typedef of struct/union
  (PR c/6660)
- fix -fverbose-asm with unnamed fields (PR c/6809)
- fix -mmmx ICE (PR optimization/6842)
- default to -momit-leaf-frame-pointer on i386 (Richard Henderson)
- use linkonce section/hidden symbol for i686 pic getpc thunks
  (Richard Henderson)

* Tue May 28 2002 Jakub Jelinek <jakub@redhat.com> 3.1-4
- rebuilt

* Sat May 25 2002 Jakub Jelinek <jakub@redhat.com> 3.1-3
- update from 3.1 branch
  - PRs other/6782, preprocessor/6780, preprocessor/6517,
	libstdc++/6282, libstdc++/6701, libstdc++/6701
  - fix out << "" bug (Ben Kosnik, #65409, PR libstdc++/6750)
- 3 new patches
  - fix C++ __PRETTY_FUNCTION__ (PR c++/6794)
  - fix ICE on jikes (#65379)
  - add test for fixed mozilla miscompilation
- include intrinsic headers on IA-32/x86-64, include altivec.h on PPC

* Wed May 22 2002 Jakub Jelinek <jakub@redhat.com> 3.1-2
- update from 3.1 branch
- 8 new patches
  - fix as version test for 2.12.1 and newer binutils non-CVS releases
  - fix ICE in do_subst (#65049)
  - fix SSE conditional move (PR target/6753)
  - fix SPARC CSE ICE (PR optimization/6759)
  - fix x86_64 dbx64_register_map typo (Jan Hubicka)
  - fix DWARF-2 with flag_asynchronous_unwind_tables set for leaf
    functions (Jan Hubicka)
  - fix DWARF-2 x86_64 __builtin_dwarf_reg_sizes (Jan Hubicka)
  - fix x86_64 movabsdi (Michael Matz)

* Wed May 15 2002 Jakub Jelinek <jakub@redhat.com> 3.1-1
- update to 3.1 final
- 15 new patches
  - fix PR c/6643
  - fix fold-const.c typo
  - fix unitialized pointer-to-member values (Alexandre Oliva)
  - fix templates with asm inputs (Jason Merrill)
  - fix -fdata-section (Andreas Schwab)
  - readd warning about i386 -malign-double into documentation (Jan Hubicka)
  - fix PR libstdc++/6594 (Ben Kosnik)
  - fix PR PR libstdc++/6648 (Paolo Carlini)
  - fix libstdc++ testsuite rlimits (Rainer Orth)
  - s390 java support (Gerhard Tonn)
  - rotate testcases (Tom Rix)
  - build libiberty with -fpic on x86_64 (Andreas Schwab)
  - fix x86_64 multilib build (Bo Thorsen)
  - fix x86_64 ASM_OUTPUT_MI_THUNK (Jan Hubicka)
  - fix loop-2[cd].c tests on i386 (Eric Botcazou)
- fix typo in g77 info files tweaking
- fix libgcj.so symlink

* Thu May  9 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.28
- update to CVS 3.1 branch
  - PR c++/6212, target/6429, opt/6534, c/6543, target/6561, c/6569
- fix x86_64 q_regs_operand (Jan Hubicka)
- better PR c++/6381 fix (Jason Merrill)

* Fri May  3 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.27
- update to CVS 3.1 branch
  - PR target/5628, libstdc++/5820, c++/6396, preprocessor/6489,
    libstdc++/6501, libstdc++/6511, target/6512, libstdc++/6513,
    bootstrap/6514, opt/6516, bootstrap/6525, c++/6527, libstdc++/6533,
    target/6540
- fix PR target/6542, target/6522, libstdc++/6549

* Mon Apr 29 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.26
- update to CVS 3.1 branch
  - PR c/3581, libstdc++/4150, libstdc++/4164, c/5154, c/5430, c++/5504,
    c++/5658, c++/5719, f/6138, libgcj/6158, middle-end/6205, c++/6256,
    c/6300, c++/6331, c/6343, c/6344, c++/6352, c/6358, libstdc++/6360,
    c++/6395, target/6413, libstdc++/6414, target/6422, bootstrap/6445,
    optimization/6475, target/6476, c++/6477, c++/6479, c++/6486, c++/6492,
    target/6494, target/6496, c/6497, target/6500
- fix PR c++/6396
- run make check as part of build process

* Thu Apr 18 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.25
- update to CVS 3.1 branch
  - PR opt/420, c++/525, target/817, target/1538, opt/3967, target/3997,
    opt/4120, bootstrap/4191, opt/4311, optimization/4328, c++/4884, c++/4934,
    c/5078, c++/5104, opt/5120, c++/5189, c++/5373, target/5446, c/5484,
    c++/5507, c++/5571, c++/5636, target/5672, target/5715, target/5886,
    c++/5933, c++/5964, c++/5998, opt/6007, target/6032, target/6041,
    target/6054, c++/6073, target/6082, optimization/6086, target/6087,
    middle-end/6096, middle-end/6098, middle-end/6099, middle-end/6100,
    middle-end/6102, fortran/6106, c++/6119, opt/6165, optimization/6177,
    c++/6179, optimization/6189, c/6202, c/6223, optimization/6233,
    middle-end/6279, c/6290, optimization/6305, target/6305, bootstrap/6315,
    c++/6320...
- fix PR c++/6316

* Wed Mar 27 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.24
- update to CVS 3.1 branch
  - PRs c/5656, c/5972, bootstrap/4192, target/4792, bootstrap/4195,
    optimization/5854, target/6043, c++/6037, bootstrap/4128, target/5740,
    c/5597, optimization/5863, optimization/5742, target/3177, c/5354,
    optimization/5999, target/5977, middle-end/5731, target/5312...

* Fri Mar 15 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.23.1
- fix info and man page generation

* Thu Mar 14 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.23
- update to CVS 3.1 branch
  - fix IA-64 packet selection (PR optimization/5892)
  - make highest_pow2_factor work for all constants (PR middle-end/5877)
  - fix -Wunused (#61047)
  - fix loop on mixed mode class assignments (#60923)
  - fix wide character literals
  - support SPARC v9 long distance branches (PR target/5626)
  - fix SPARC leaf functions
  - fix a rtl sharing problem (Richard Henderson, #60760,
    PR optimization/5844)
  - fix va_arg with variable size types (PR c/3711)
  - PRs optimization/5901, optimization/5878, 5693, preprocessor/5899
- fix C++ ?: at the end of stmt expr (PR c++/5373)
- fix loop unrolling with sibcalls (PR optimization/5891)

* Thu Mar  7 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.22
- update to CVS 3.1 branch
  - fix ICE with volatile long long (#60650)
  - fix tempbuf.h (Philipp Thomas, #60212)
  - fix -fssa-ccp (Jeff Law, #60651)
  - versioned libstdc++
  - backport __attribute__((visibility("..."))) patches from trunk
- include libstdc++ html documentation

* Tue Feb  5 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.21
- update to CVS HEAD
  - fix demangler (H.J. Lu, #59300, #59310)
  - fix typo in IA-32 specs file (#59081)
  - support moving SFmode values in MMX regs if -mmmx (#59083)
  - fix recog_for_combine (#59084)
  - don't ICE when inserting insns on edge from bb0 to bb0 (Bernd Schmidt,
    #59087)
  - make sure configure has not time in the future (#59203)
  - fix division/modulo by certain constants (#58065, PR c/5304)
  - fix -Wswitch (PR c/4475)

* Thu Jan 31 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.20
- update to CVS HEAD
  - fix jar (Tom Tromey)
  - fix loop unrolling (Richard Henderson)

* Wed Jan 30 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.19
- update to CVS HEAD
  - fix a reload bug on ia32 (#58579, #58648)
  - issue error about unknown -W* options (#58909)
  - fix ia64 libbfd miscompilation (#58694)
  - register all pending unparsed_text structures with GC (#58647)
  - fix __builtin_apply with ia32 -msse (#58447)
  - prevent ia64 prologue insns saving regs required for eh from being
    deleted (#58387)

* Tue Jan 15 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.18
- update to CVS HEAD
  - handle static x[] = { [X...Y] = (foo) { Z } } (#58338)
  - fix getdents.os miscompilation (Richard Henderson, #58308)
  - fix ICE in try_forward_edges (#58125)
  - fix ICE with -fexceptions -foptimize-sibling-calls

* Tue Jan  8 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.17
- avoid division by 0 when computing prediction probabilities (#57992)
- fix ICE due to store_expr not adjusting value back for mode
- increase -ftemplate-depth default value to 500

* Mon Jan  7 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.16
- if using PT_GNU_EH_FRAME registry, work around assembler bug resp. feature
  and don't provide weak prototypes of functions which won't be used
- on Alpha, fix a typo so that crtbeginT.o is built and installed
- fix glibc inl-tester miscompilation on ia32

* Sun Jan  6 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.15
- update to CVS HEAD (fix glibc bootstrap failure)

* Thu Jan  3 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.14
- update to CVS HEAD (#57907)
  - fix alpha bootstrap (Richard Henderson)
- fix simplification of (div:SI (???:DI ???) (const_int 1))
  (#57916)
- add contrib/gcc_update --touch

* Tue Jan  1 2002 Jakub Jelinek <jakub@redhat.com> 3.1-0.13
- update to CVS HEAD (fix glibc miscompilation on alpha)
- fix objc to not emit __objc_class_name_* without type and size

* Mon Dec 31 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.12
- update to CVS HEAD
- fix sed commands for .la files
- make Alpha use PT_GNU_EH_FRAME

* Thu Dec 27 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.11
- update to CVS HEAD (#57165, #57212, #57467, #57488, #57502,
  #57505, #57574)
- readd .la files after fixing them up by sed
- add %%defattr(-,root,root) to libobjc subpackage

* Mon Dec  3 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.10
- one more gcc.spec fix for passing --gdwarf-2 resp. --gstabs to as
- fix conditional register dead computation on IA-64
- fix extern array of incomplete structures handling
- fix gcc -xc -
- fix Fortran ICEs with SAVE_EXPRs (Richard Kenner)

* Tue Nov 27 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.9
- update to CVS HEAD
- make DWARF 2 preferred debugging format on Linux

* Mon Nov 12 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.8
- don't ship .la files (#56072)
- include libfrtbegin.a (#56098)

* Mon Nov 12 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.7
- update to CVS HEAD
- back out Nov 7th loop.c change for now

* Fri Nov  9 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.6
- update to CVS HEAD
- frame unwind compatibility with 7.[12] binutils

* Tue Nov  6 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.5
- update to CVS HEAD
- merge DW_EH_PE_indirect constants and their relocs

* Thu Oct 25 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.4
- don't loop forever or ICE on bogus array initializers (#53704)
- fix store motion with pure calls
- disable store motion for now

* Tue Oct 23 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.3
- fix inlining of C nested functions with auto prototypes

* Mon Oct 22 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.2
- update to CVS HEAD
- tree inlining fix from Alexandre Oliva
- fix anonymous union ICE on alpha

* Mon Oct 15 2001 Jakub Jelinek <jakub@redhat.com> 3.1-0.1
- switch package to main compiler from alternate compiler
- update to CVS HEAD
- early gcc-2.96-RH compatibility in __frame_state_for
- change weak function tests for functions always present in GLIBC 2.2
  into simple non-weak calls in crt*.o to avoid unnecessary symbol
  lookups and prelink conflicts
- don't link against libgcc_s C shared libraries

* Tue Oct  2 2001 Jakub Jelinek <jakub@redhat.com> 3.0.1-4
- update from CVS 3.0 branch
  - ia64 function descriptors in vtables
- handle large files in Fortran (#53328)
- allow Java programs to be statically linked (#53605)
- remove #include_next patch, Benjamin commited it

* Thu Sep  6 2001 Jakub Jelinek <jakub@redhat.com> 3.0.1-3
- don't use #include_next in <bits/std_c*> headers (Benjamin Kosnik, #53262)

* Wed Sep  5 2001 Jakub Jelinek <jakub@redhat.com> 3.0.1-2
- update from CVS 3.0 branch
- check all gcc-2.96-RH patches whether they have made it into 3.0.1,
  and if not, whether they are appropriate for 3.0.1
- 8 new patches
  - add 36 testcases from gcc-2.96-RH
  - fix ICE on very questionable C++ code from JDK (#39858, #52960)
  - fix -frepo (Nathan Sidwell, #52877)
  - avoid generating bogus .stabs (#49214)
  - issue a clear error message about invalid ia32 floating point
    asm constraints (#27137)
  - fix some comment typos
  - fix ADDRESSOF recognition (#29686)

* Mon Aug 27 2001 Jakub Jelinek <jakub@redhat.com> 3.0.1-1
- update from CVS (3.0.1 final)
- properly handle throw() exception specifiers in template decls (#51824)
- fix IA-64 varargs handling in presence of additional anonymous arguments
  (#50757)
- fix boehm-gc for prelink
- fix a typo in gcc3-c++ description (#52323)
- remove Chill from package summary (#51764)

* Tue Aug  7 2001 Jakub Jelinek <jakub@redhat.com> 3.0-6
- update from CVS
  - fix glibc vfprintf miscompilation
- don't warn about if (&foo) if foo is weak (H.J.Lu, #50855)

* Wed Jul 25 2001 Jakub Jelinek <jakub@redhat.com> 3.0-5
- include libgcjgc.a in libgcj3-devel
- include libgcjgc.so.* in libgcj3 on ia64
- remove dependency on libgcj on ia64
- add ldconfig to libgcj3 post/postun

* Tue Jul 24 2001 Jakub Jelinek <jakub@redhat.com> 3.0-4
- update from CVS
- make gcc3-java/libgcj3* packages, so that they can coexist
  with 2.96-RH Java
- make sure shared Java libraries are built with proper dependencies

* Wed Jul 11 2001 Jakub Jelinek <jakub@redhat.com> 3.0-3
- fix libgcc_s.so and libstdc++.so symlinks
- don't ship jar

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com> 3.0-2
- move libstdc++.so into gcc-lib
- add libobjc.so symlink

* Tue Jul 10 2001 Jakub Jelinek <jakub@redhat.com> 3.0-1
- new rpm
