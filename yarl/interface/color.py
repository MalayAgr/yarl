"""
Module which provides some RGB color constants and a `namedtuple` to represent colors.


Available Colors:

| Name | Value |
|---|---|
| aliceblue | [RGB][yarl.interface.color.RGB](red=240, green=248, blue=255) |
| antiquewhite | [RGB][yarl.interface.color.RGB](red=250, green=235, blue=215) |
| antiquewhite1 | [RGB][yarl.interface.color.RGB](red=255, green=239, blue=219) |
| antiquewhite2 | [RGB][yarl.interface.color.RGB](red=238, green=223, blue=204) |
| antiquewhite3 | [RGB][yarl.interface.color.RGB](red=205, green=192, blue=176) |
| antiquewhite4 | [RGB][yarl.interface.color.RGB](red=139, green=131, blue=120) |
| aqua | [RGB][yarl.interface.color.RGB](red=0, green=255, blue=255) |
| aquamarine1 | [RGB][yarl.interface.color.RGB](red=127, green=255, blue=212) |
| aquamarine2 | [RGB][yarl.interface.color.RGB](red=118, green=238, blue=198) |
| aquamarine3 | [RGB][yarl.interface.color.RGB](red=102, green=205, blue=170) |
| aquamarine4 | [RGB][yarl.interface.color.RGB](red=69, green=139, blue=116) |
| azure1 | [RGB][yarl.interface.color.RGB](red=240, green=255, blue=255) |
| azure2 | [RGB][yarl.interface.color.RGB](red=224, green=238, blue=238) |
| azure3 | [RGB][yarl.interface.color.RGB](red=193, green=205, blue=205) |
| azure4 | [RGB][yarl.interface.color.RGB](red=131, green=139, blue=139) |
| banana | [RGB][yarl.interface.color.RGB](red=227, green=207, blue=87) |
| beige | [RGB][yarl.interface.color.RGB](red=245, green=245, blue=220) |
| bisque1 | [RGB][yarl.interface.color.RGB](red=255, green=228, blue=196) |
| bisque2 | [RGB][yarl.interface.color.RGB](red=238, green=213, blue=183) |
| bisque3 | [RGB][yarl.interface.color.RGB](red=205, green=183, blue=158) |
| bisque4 | [RGB][yarl.interface.color.RGB](red=139, green=125, blue=107) |
| black | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=0) |
| blanchedalmond | [RGB][yarl.interface.color.RGB](red=255, green=235, blue=205) |
| blue | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=255) |
| blue2 | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=238) |
| blue3 | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=205) |
| blue4 | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=139) |
| blueviolet | [RGB][yarl.interface.color.RGB](red=138, green=43, blue=226) |
| brick | [RGB][yarl.interface.color.RGB](red=156, green=102, blue=31) |
| brown | [RGB][yarl.interface.color.RGB](red=165, green=42, blue=42) |
| brown1 | [RGB][yarl.interface.color.RGB](red=255, green=64, blue=64) |
| brown2 | [RGB][yarl.interface.color.RGB](red=238, green=59, blue=59) |
| brown3 | [RGB][yarl.interface.color.RGB](red=205, green=51, blue=51) |
| brown4 | [RGB][yarl.interface.color.RGB](red=139, green=35, blue=35) |
| burlywood | [RGB][yarl.interface.color.RGB](red=222, green=184, blue=135) |
| burlywood1 | [RGB][yarl.interface.color.RGB](red=255, green=211, blue=155) |
| burlywood2 | [RGB][yarl.interface.color.RGB](red=238, green=197, blue=145) |
| burlywood3 | [RGB][yarl.interface.color.RGB](red=205, green=170, blue=125) |
| burlywood4 | [RGB][yarl.interface.color.RGB](red=139, green=115, blue=85) |
| burntsienna | [RGB][yarl.interface.color.RGB](red=138, green=54, blue=15) |
| burntumber | [RGB][yarl.interface.color.RGB](red=138, green=51, blue=36) |
| cadetblue | [RGB][yarl.interface.color.RGB](red=95, green=158, blue=160) |
| cadetblue1 | [RGB][yarl.interface.color.RGB](red=152, green=245, blue=255) |
| cadetblue2 | [RGB][yarl.interface.color.RGB](red=142, green=229, blue=238) |
| cadetblue3 | [RGB][yarl.interface.color.RGB](red=122, green=197, blue=205) |
| cadetblue4 | [RGB][yarl.interface.color.RGB](red=83, green=134, blue=139) |
| cadmiumorange | [RGB][yarl.interface.color.RGB](red=255, green=97, blue=3) |
| cadmiumyellow | [RGB][yarl.interface.color.RGB](red=255, green=153, blue=18) |
| carrot | [RGB][yarl.interface.color.RGB](red=237, green=145, blue=33) |
| chartreuse1 | [RGB][yarl.interface.color.RGB](red=127, green=255, blue=0) |
| chartreuse2 | [RGB][yarl.interface.color.RGB](red=118, green=238, blue=0) |
| chartreuse3 | [RGB][yarl.interface.color.RGB](red=102, green=205, blue=0) |
| chartreuse4 | [RGB][yarl.interface.color.RGB](red=69, green=139, blue=0) |
| chocolate | [RGB][yarl.interface.color.RGB](red=210, green=105, blue=30) |
| chocolate1 | [RGB][yarl.interface.color.RGB](red=255, green=127, blue=36) |
| chocolate2 | [RGB][yarl.interface.color.RGB](red=238, green=118, blue=33) |
| chocolate3 | [RGB][yarl.interface.color.RGB](red=205, green=102, blue=29) |
| chocolate4 | [RGB][yarl.interface.color.RGB](red=139, green=69, blue=19) |
| cobalt | [RGB][yarl.interface.color.RGB](red=61, green=89, blue=171) |
| cobaltgreen | [RGB][yarl.interface.color.RGB](red=61, green=145, blue=64) |
| coldgrey | [RGB][yarl.interface.color.RGB](red=128, green=138, blue=135) |
| coral | [RGB][yarl.interface.color.RGB](red=255, green=127, blue=80) |
| coral1 | [RGB][yarl.interface.color.RGB](red=255, green=114, blue=86) |
| coral2 | [RGB][yarl.interface.color.RGB](red=238, green=106, blue=80) |
| coral3 | [RGB][yarl.interface.color.RGB](red=205, green=91, blue=69) |
| coral4 | [RGB][yarl.interface.color.RGB](red=139, green=62, blue=47) |
| cornflowerblue | [RGB][yarl.interface.color.RGB](red=100, green=149, blue=237) |
| cornsilk1 | [RGB][yarl.interface.color.RGB](red=255, green=248, blue=220) |
| cornsilk2 | [RGB][yarl.interface.color.RGB](red=238, green=232, blue=205) |
| cornsilk3 | [RGB][yarl.interface.color.RGB](red=205, green=200, blue=177) |
| cornsilk4 | [RGB][yarl.interface.color.RGB](red=139, green=136, blue=120) |
| crimson | [RGB][yarl.interface.color.RGB](red=220, green=20, blue=60) |
| cyan2 | [RGB][yarl.interface.color.RGB](red=0, green=238, blue=238) |
| cyan3 | [RGB][yarl.interface.color.RGB](red=0, green=205, blue=205) |
| cyan4 | [RGB][yarl.interface.color.RGB](red=0, green=139, blue=139) |
| darkgoldenrod | [RGB][yarl.interface.color.RGB](red=184, green=134, blue=11) |
| darkgoldenrod1 | [RGB][yarl.interface.color.RGB](red=255, green=185, blue=15) |
| darkgoldenrod2 | [RGB][yarl.interface.color.RGB](red=238, green=173, blue=14) |
| darkgoldenrod3 | [RGB][yarl.interface.color.RGB](red=205, green=149, blue=12) |
| darkgoldenrod4 | [RGB][yarl.interface.color.RGB](red=139, green=101, blue=8) |
| darkgray | [RGB][yarl.interface.color.RGB](red=169, green=169, blue=169) |
| darkgreen | [RGB][yarl.interface.color.RGB](red=0, green=100, blue=0) |
| darkkhaki | [RGB][yarl.interface.color.RGB](red=189, green=183, blue=107) |
| darkolivegreen | [RGB][yarl.interface.color.RGB](red=85, green=107, blue=47) |
| darkolivegreen1 | [RGB][yarl.interface.color.RGB](red=202, green=255, blue=112) |
| darkolivegreen2 | [RGB][yarl.interface.color.RGB](red=188, green=238, blue=104) |
| darkolivegreen3 | [RGB][yarl.interface.color.RGB](red=162, green=205, blue=90) |
| darkolivegreen4 | [RGB][yarl.interface.color.RGB](red=110, green=139, blue=61) |
| darkorange | [RGB][yarl.interface.color.RGB](red=255, green=140, blue=0) |
| darkorange1 | [RGB][yarl.interface.color.RGB](red=255, green=127, blue=0) |
| darkorange2 | [RGB][yarl.interface.color.RGB](red=238, green=118, blue=0) |
| darkorange3 | [RGB][yarl.interface.color.RGB](red=205, green=102, blue=0) |
| darkorange4 | [RGB][yarl.interface.color.RGB](red=139, green=69, blue=0) |
| darkorchid | [RGB][yarl.interface.color.RGB](red=153, green=50, blue=204) |
| darkorchid1 | [RGB][yarl.interface.color.RGB](red=191, green=62, blue=255) |
| darkorchid2 | [RGB][yarl.interface.color.RGB](red=178, green=58, blue=238) |
| darkorchid3 | [RGB][yarl.interface.color.RGB](red=154, green=50, blue=205) |
| darkorchid4 | [RGB][yarl.interface.color.RGB](red=104, green=34, blue=139) |
| darksalmon | [RGB][yarl.interface.color.RGB](red=233, green=150, blue=122) |
| darkseagreen | [RGB][yarl.interface.color.RGB](red=143, green=188, blue=143) |
| darkseagreen1 | [RGB][yarl.interface.color.RGB](red=193, green=255, blue=193) |
| darkseagreen2 | [RGB][yarl.interface.color.RGB](red=180, green=238, blue=180) |
| darkseagreen3 | [RGB][yarl.interface.color.RGB](red=155, green=205, blue=155) |
| darkseagreen4 | [RGB][yarl.interface.color.RGB](red=105, green=139, blue=105) |
| darkslateblue | [RGB][yarl.interface.color.RGB](red=72, green=61, blue=139) |
| darkslategray | [RGB][yarl.interface.color.RGB](red=47, green=79, blue=79) |
| darkslategray1 | [RGB][yarl.interface.color.RGB](red=151, green=255, blue=255) |
| darkslategray2 | [RGB][yarl.interface.color.RGB](red=141, green=238, blue=238) |
| darkslategray3 | [RGB][yarl.interface.color.RGB](red=121, green=205, blue=205) |
| darkslategray4 | [RGB][yarl.interface.color.RGB](red=82, green=139, blue=139) |
| darkturquoise | [RGB][yarl.interface.color.RGB](red=0, green=206, blue=209) |
| darkviolet | [RGB][yarl.interface.color.RGB](red=148, green=0, blue=211) |
| deeppink1 | [RGB][yarl.interface.color.RGB](red=255, green=20, blue=147) |
| deeppink2 | [RGB][yarl.interface.color.RGB](red=238, green=18, blue=137) |
| deeppink3 | [RGB][yarl.interface.color.RGB](red=205, green=16, blue=118) |
| deeppink4 | [RGB][yarl.interface.color.RGB](red=139, green=10, blue=80) |
| deepskyblue1 | [RGB][yarl.interface.color.RGB](red=0, green=191, blue=255) |
| deepskyblue2 | [RGB][yarl.interface.color.RGB](red=0, green=178, blue=238) |
| deepskyblue3 | [RGB][yarl.interface.color.RGB](red=0, green=154, blue=205) |
| deepskyblue4 | [RGB][yarl.interface.color.RGB](red=0, green=104, blue=139) |
| dimgray | [RGB][yarl.interface.color.RGB](red=105, green=105, blue=105) |
| dodgerblue1 | [RGB][yarl.interface.color.RGB](red=30, green=144, blue=255) |
| dodgerblue2 | [RGB][yarl.interface.color.RGB](red=28, green=134, blue=238) |
| dodgerblue3 | [RGB][yarl.interface.color.RGB](red=24, green=116, blue=205) |
| dodgerblue4 | [RGB][yarl.interface.color.RGB](red=16, green=78, blue=139) |
| eggshell | [RGB][yarl.interface.color.RGB](red=252, green=230, blue=201) |
| emeraldgreen | [RGB][yarl.interface.color.RGB](red=0, green=201, blue=87) |
| firebrick | [RGB][yarl.interface.color.RGB](red=178, green=34, blue=34) |
| firebrick1 | [RGB][yarl.interface.color.RGB](red=255, green=48, blue=48) |
| firebrick2 | [RGB][yarl.interface.color.RGB](red=238, green=44, blue=44) |
| firebrick3 | [RGB][yarl.interface.color.RGB](red=205, green=38, blue=38) |
| firebrick4 | [RGB][yarl.interface.color.RGB](red=139, green=26, blue=26) |
| flesh | [RGB][yarl.interface.color.RGB](red=255, green=125, blue=64) |
| floralwhite | [RGB][yarl.interface.color.RGB](red=255, green=250, blue=240) |
| forestgreen | [RGB][yarl.interface.color.RGB](red=34, green=139, blue=34) |
| gainsboro | [RGB][yarl.interface.color.RGB](red=220, green=220, blue=220) |
| ghostwhite | [RGB][yarl.interface.color.RGB](red=248, green=248, blue=255) |
| gold1 | [RGB][yarl.interface.color.RGB](red=255, green=215, blue=0) |
| gold2 | [RGB][yarl.interface.color.RGB](red=238, green=201, blue=0) |
| gold3 | [RGB][yarl.interface.color.RGB](red=205, green=173, blue=0) |
| gold4 | [RGB][yarl.interface.color.RGB](red=139, green=117, blue=0) |
| goldenrod | [RGB][yarl.interface.color.RGB](red=218, green=165, blue=32) |
| goldenrod1 | [RGB][yarl.interface.color.RGB](red=255, green=193, blue=37) |
| goldenrod2 | [RGB][yarl.interface.color.RGB](red=238, green=180, blue=34) |
| goldenrod3 | [RGB][yarl.interface.color.RGB](red=205, green=155, blue=29) |
| goldenrod4 | [RGB][yarl.interface.color.RGB](red=139, green=105, blue=20) |
| gray | [RGB][yarl.interface.color.RGB](red=128, green=128, blue=128) |
| gray1 | [RGB][yarl.interface.color.RGB](red=3, green=3, blue=3) |
| gray10 | [RGB][yarl.interface.color.RGB](red=26, green=26, blue=26) |
| gray11 | [RGB][yarl.interface.color.RGB](red=28, green=28, blue=28) |
| gray12 | [RGB][yarl.interface.color.RGB](red=31, green=31, blue=31) |
| gray13 | [RGB][yarl.interface.color.RGB](red=33, green=33, blue=33) |
| gray14 | [RGB][yarl.interface.color.RGB](red=36, green=36, blue=36) |
| gray15 | [RGB][yarl.interface.color.RGB](red=38, green=38, blue=38) |
| gray16 | [RGB][yarl.interface.color.RGB](red=41, green=41, blue=41) |
| gray17 | [RGB][yarl.interface.color.RGB](red=43, green=43, blue=43) |
| gray18 | [RGB][yarl.interface.color.RGB](red=46, green=46, blue=46) |
| gray19 | [RGB][yarl.interface.color.RGB](red=48, green=48, blue=48) |
| gray2 | [RGB][yarl.interface.color.RGB](red=5, green=5, blue=5) |
| gray20 | [RGB][yarl.interface.color.RGB](red=51, green=51, blue=51) |
| gray21 | [RGB][yarl.interface.color.RGB](red=54, green=54, blue=54) |
| gray22 | [RGB][yarl.interface.color.RGB](red=56, green=56, blue=56) |
| gray23 | [RGB][yarl.interface.color.RGB](red=59, green=59, blue=59) |
| gray24 | [RGB][yarl.interface.color.RGB](red=61, green=61, blue=61) |
| gray25 | [RGB][yarl.interface.color.RGB](red=64, green=64, blue=64) |
| gray26 | [RGB][yarl.interface.color.RGB](red=66, green=66, blue=66) |
| gray27 | [RGB][yarl.interface.color.RGB](red=69, green=69, blue=69) |
| gray28 | [RGB][yarl.interface.color.RGB](red=71, green=71, blue=71) |
| gray29 | [RGB][yarl.interface.color.RGB](red=74, green=74, blue=74) |
| gray3 | [RGB][yarl.interface.color.RGB](red=8, green=8, blue=8) |
| gray30 | [RGB][yarl.interface.color.RGB](red=77, green=77, blue=77) |
| gray31 | [RGB][yarl.interface.color.RGB](red=79, green=79, blue=79) |
| gray32 | [RGB][yarl.interface.color.RGB](red=82, green=82, blue=82) |
| gray33 | [RGB][yarl.interface.color.RGB](red=84, green=84, blue=84) |
| gray34 | [RGB][yarl.interface.color.RGB](red=87, green=87, blue=87) |
| gray35 | [RGB][yarl.interface.color.RGB](red=89, green=89, blue=89) |
| gray36 | [RGB][yarl.interface.color.RGB](red=92, green=92, blue=92) |
| gray37 | [RGB][yarl.interface.color.RGB](red=94, green=94, blue=94) |
| gray38 | [RGB][yarl.interface.color.RGB](red=97, green=97, blue=97) |
| gray39 | [RGB][yarl.interface.color.RGB](red=99, green=99, blue=99) |
| gray4 | [RGB][yarl.interface.color.RGB](red=10, green=10, blue=10) |
| gray40 | [RGB][yarl.interface.color.RGB](red=102, green=102, blue=102) |
| gray42 | [RGB][yarl.interface.color.RGB](red=107, green=107, blue=107) |
| gray43 | [RGB][yarl.interface.color.RGB](red=110, green=110, blue=110) |
| gray44 | [RGB][yarl.interface.color.RGB](red=112, green=112, blue=112) |
| gray45 | [RGB][yarl.interface.color.RGB](red=115, green=115, blue=115) |
| gray46 | [RGB][yarl.interface.color.RGB](red=117, green=117, blue=117) |
| gray47 | [RGB][yarl.interface.color.RGB](red=120, green=120, blue=120) |
| gray48 | [RGB][yarl.interface.color.RGB](red=122, green=122, blue=122) |
| gray49 | [RGB][yarl.interface.color.RGB](red=125, green=125, blue=125) |
| gray5 | [RGB][yarl.interface.color.RGB](red=13, green=13, blue=13) |
| gray50 | [RGB][yarl.interface.color.RGB](red=127, green=127, blue=127) |
| gray51 | [RGB][yarl.interface.color.RGB](red=130, green=130, blue=130) |
| gray52 | [RGB][yarl.interface.color.RGB](red=133, green=133, blue=133) |
| gray53 | [RGB][yarl.interface.color.RGB](red=135, green=135, blue=135) |
| gray54 | [RGB][yarl.interface.color.RGB](red=138, green=138, blue=138) |
| gray55 | [RGB][yarl.interface.color.RGB](red=140, green=140, blue=140) |
| gray56 | [RGB][yarl.interface.color.RGB](red=143, green=143, blue=143) |
| gray57 | [RGB][yarl.interface.color.RGB](red=145, green=145, blue=145) |
| gray58 | [RGB][yarl.interface.color.RGB](red=148, green=148, blue=148) |
| gray59 | [RGB][yarl.interface.color.RGB](red=150, green=150, blue=150) |
| gray6 | [RGB][yarl.interface.color.RGB](red=15, green=15, blue=15) |
| gray60 | [RGB][yarl.interface.color.RGB](red=153, green=153, blue=153) |
| gray61 | [RGB][yarl.interface.color.RGB](red=156, green=156, blue=156) |
| gray62 | [RGB][yarl.interface.color.RGB](red=158, green=158, blue=158) |
| gray63 | [RGB][yarl.interface.color.RGB](red=161, green=161, blue=161) |
| gray64 | [RGB][yarl.interface.color.RGB](red=163, green=163, blue=163) |
| gray65 | [RGB][yarl.interface.color.RGB](red=166, green=166, blue=166) |
| gray66 | [RGB][yarl.interface.color.RGB](red=168, green=168, blue=168) |
| gray67 | [RGB][yarl.interface.color.RGB](red=171, green=171, blue=171) |
| gray68 | [RGB][yarl.interface.color.RGB](red=173, green=173, blue=173) |
| gray69 | [RGB][yarl.interface.color.RGB](red=176, green=176, blue=176) |
| gray7 | [RGB][yarl.interface.color.RGB](red=18, green=18, blue=18) |
| gray70 | [RGB][yarl.interface.color.RGB](red=179, green=179, blue=179) |
| gray71 | [RGB][yarl.interface.color.RGB](red=181, green=181, blue=181) |
| gray72 | [RGB][yarl.interface.color.RGB](red=184, green=184, blue=184) |
| gray73 | [RGB][yarl.interface.color.RGB](red=186, green=186, blue=186) |
| gray74 | [RGB][yarl.interface.color.RGB](red=189, green=189, blue=189) |
| gray75 | [RGB][yarl.interface.color.RGB](red=191, green=191, blue=191) |
| gray76 | [RGB][yarl.interface.color.RGB](red=194, green=194, blue=194) |
| gray77 | [RGB][yarl.interface.color.RGB](red=196, green=196, blue=196) |
| gray78 | [RGB][yarl.interface.color.RGB](red=199, green=199, blue=199) |
| gray79 | [RGB][yarl.interface.color.RGB](red=201, green=201, blue=201) |
| gray8 | [RGB][yarl.interface.color.RGB](red=20, green=20, blue=20) |
| gray80 | [RGB][yarl.interface.color.RGB](red=204, green=204, blue=204) |
| gray81 | [RGB][yarl.interface.color.RGB](red=207, green=207, blue=207) |
| gray82 | [RGB][yarl.interface.color.RGB](red=209, green=209, blue=209) |
| gray83 | [RGB][yarl.interface.color.RGB](red=212, green=212, blue=212) |
| gray84 | [RGB][yarl.interface.color.RGB](red=214, green=214, blue=214) |
| gray85 | [RGB][yarl.interface.color.RGB](red=217, green=217, blue=217) |
| gray86 | [RGB][yarl.interface.color.RGB](red=219, green=219, blue=219) |
| gray87 | [RGB][yarl.interface.color.RGB](red=222, green=222, blue=222) |
| gray88 | [RGB][yarl.interface.color.RGB](red=224, green=224, blue=224) |
| gray89 | [RGB][yarl.interface.color.RGB](red=227, green=227, blue=227) |
| gray9 | [RGB][yarl.interface.color.RGB](red=23, green=23, blue=23) |
| gray90 | [RGB][yarl.interface.color.RGB](red=229, green=229, blue=229) |
| gray91 | [RGB][yarl.interface.color.RGB](red=232, green=232, blue=232) |
| gray92 | [RGB][yarl.interface.color.RGB](red=235, green=235, blue=235) |
| gray93 | [RGB][yarl.interface.color.RGB](red=237, green=237, blue=237) |
| gray94 | [RGB][yarl.interface.color.RGB](red=240, green=240, blue=240) |
| gray95 | [RGB][yarl.interface.color.RGB](red=242, green=242, blue=242) |
| gray97 | [RGB][yarl.interface.color.RGB](red=247, green=247, blue=247) |
| gray98 | [RGB][yarl.interface.color.RGB](red=250, green=250, blue=250) |
| gray99 | [RGB][yarl.interface.color.RGB](red=252, green=252, blue=252) |
| green | [RGB][yarl.interface.color.RGB](red=0, green=128, blue=0) |
| green1 | [RGB][yarl.interface.color.RGB](red=0, green=255, blue=0) |
| green2 | [RGB][yarl.interface.color.RGB](red=0, green=238, blue=0) |
| green3 | [RGB][yarl.interface.color.RGB](red=0, green=205, blue=0) |
| green4 | [RGB][yarl.interface.color.RGB](red=0, green=139, blue=0) |
| greenyellow | [RGB][yarl.interface.color.RGB](red=173, green=255, blue=47) |
| honeydew1 | [RGB][yarl.interface.color.RGB](red=240, green=255, blue=240) |
| honeydew2 | [RGB][yarl.interface.color.RGB](red=224, green=238, blue=224) |
| honeydew3 | [RGB][yarl.interface.color.RGB](red=193, green=205, blue=193) |
| honeydew4 | [RGB][yarl.interface.color.RGB](red=131, green=139, blue=131) |
| hotpink | [RGB][yarl.interface.color.RGB](red=255, green=105, blue=180) |
| hotpink1 | [RGB][yarl.interface.color.RGB](red=255, green=110, blue=180) |
| hotpink2 | [RGB][yarl.interface.color.RGB](red=238, green=106, blue=167) |
| hotpink3 | [RGB][yarl.interface.color.RGB](red=205, green=96, blue=144) |
| hotpink4 | [RGB][yarl.interface.color.RGB](red=139, green=58, blue=98) |
| indianred | [RGB][yarl.interface.color.RGB](red=205, green=92, blue=92) |
| indianred1 | [RGB][yarl.interface.color.RGB](red=255, green=106, blue=106) |
| indianred2 | [RGB][yarl.interface.color.RGB](red=238, green=99, blue=99) |
| indianred3 | [RGB][yarl.interface.color.RGB](red=205, green=85, blue=85) |
| indianred4 | [RGB][yarl.interface.color.RGB](red=139, green=58, blue=58) |
| indigo | [RGB][yarl.interface.color.RGB](red=75, green=0, blue=130) |
| ivory1 | [RGB][yarl.interface.color.RGB](red=255, green=255, blue=240) |
| ivory2 | [RGB][yarl.interface.color.RGB](red=238, green=238, blue=224) |
| ivory3 | [RGB][yarl.interface.color.RGB](red=205, green=205, blue=193) |
| ivory4 | [RGB][yarl.interface.color.RGB](red=139, green=139, blue=131) |
| ivoryblack | [RGB][yarl.interface.color.RGB](red=41, green=36, blue=33) |
| khaki | [RGB][yarl.interface.color.RGB](red=240, green=230, blue=140) |
| khaki1 | [RGB][yarl.interface.color.RGB](red=255, green=246, blue=143) |
| khaki2 | [RGB][yarl.interface.color.RGB](red=238, green=230, blue=133) |
| khaki3 | [RGB][yarl.interface.color.RGB](red=205, green=198, blue=115) |
| khaki4 | [RGB][yarl.interface.color.RGB](red=139, green=134, blue=78) |
| lavender | [RGB][yarl.interface.color.RGB](red=230, green=230, blue=250) |
| lavenderblush1 | [RGB][yarl.interface.color.RGB](red=255, green=240, blue=245) |
| lavenderblush2 | [RGB][yarl.interface.color.RGB](red=238, green=224, blue=229) |
| lavenderblush3 | [RGB][yarl.interface.color.RGB](red=205, green=193, blue=197) |
| lavenderblush4 | [RGB][yarl.interface.color.RGB](red=139, green=131, blue=134) |
| lawngreen | [RGB][yarl.interface.color.RGB](red=124, green=252, blue=0) |
| lemonchiffon1 | [RGB][yarl.interface.color.RGB](red=255, green=250, blue=205) |
| lemonchiffon2 | [RGB][yarl.interface.color.RGB](red=238, green=233, blue=191) |
| lemonchiffon3 | [RGB][yarl.interface.color.RGB](red=205, green=201, blue=165) |
| lemonchiffon4 | [RGB][yarl.interface.color.RGB](red=139, green=137, blue=112) |
| lightblue | [RGB][yarl.interface.color.RGB](red=173, green=216, blue=230) |
| lightblue1 | [RGB][yarl.interface.color.RGB](red=191, green=239, blue=255) |
| lightblue2 | [RGB][yarl.interface.color.RGB](red=178, green=223, blue=238) |
| lightblue3 | [RGB][yarl.interface.color.RGB](red=154, green=192, blue=205) |
| lightblue4 | [RGB][yarl.interface.color.RGB](red=104, green=131, blue=139) |
| lightcoral | [RGB][yarl.interface.color.RGB](red=240, green=128, blue=128) |
| lightcyan1 | [RGB][yarl.interface.color.RGB](red=224, green=255, blue=255) |
| lightcyan2 | [RGB][yarl.interface.color.RGB](red=209, green=238, blue=238) |
| lightcyan3 | [RGB][yarl.interface.color.RGB](red=180, green=205, blue=205) |
| lightcyan4 | [RGB][yarl.interface.color.RGB](red=122, green=139, blue=139) |
| lightgoldenrod1 | [RGB][yarl.interface.color.RGB](red=255, green=236, blue=139) |
| lightgoldenrod2 | [RGB][yarl.interface.color.RGB](red=238, green=220, blue=130) |
| lightgoldenrod3 | [RGB][yarl.interface.color.RGB](red=205, green=190, blue=112) |
| lightgoldenrod4 | [RGB][yarl.interface.color.RGB](red=139, green=129, blue=76) |
| lightgoldenrodyellow | [RGB][yarl.interface.color.RGB](red=250, green=250, blue=210) |
| lightgrey | [RGB][yarl.interface.color.RGB](red=211, green=211, blue=211) |
| lightpink | [RGB][yarl.interface.color.RGB](red=255, green=182, blue=193) |
| lightpink1 | [RGB][yarl.interface.color.RGB](red=255, green=174, blue=185) |
| lightpink2 | [RGB][yarl.interface.color.RGB](red=238, green=162, blue=173) |
| lightpink3 | [RGB][yarl.interface.color.RGB](red=205, green=140, blue=149) |
| lightpink4 | [RGB][yarl.interface.color.RGB](red=139, green=95, blue=101) |
| lightsalmon1 | [RGB][yarl.interface.color.RGB](red=255, green=160, blue=122) |
| lightsalmon2 | [RGB][yarl.interface.color.RGB](red=238, green=149, blue=114) |
| lightsalmon3 | [RGB][yarl.interface.color.RGB](red=205, green=129, blue=98) |
| lightsalmon4 | [RGB][yarl.interface.color.RGB](red=139, green=87, blue=66) |
| lightseagreen | [RGB][yarl.interface.color.RGB](red=32, green=178, blue=170) |
| lightskyblue | [RGB][yarl.interface.color.RGB](red=135, green=206, blue=250) |
| lightskyblue1 | [RGB][yarl.interface.color.RGB](red=176, green=226, blue=255) |
| lightskyblue2 | [RGB][yarl.interface.color.RGB](red=164, green=211, blue=238) |
| lightskyblue3 | [RGB][yarl.interface.color.RGB](red=141, green=182, blue=205) |
| lightskyblue4 | [RGB][yarl.interface.color.RGB](red=96, green=123, blue=139) |
| lightslateblue | [RGB][yarl.interface.color.RGB](red=132, green=112, blue=255) |
| lightslategray | [RGB][yarl.interface.color.RGB](red=119, green=136, blue=153) |
| lightsteelblue | [RGB][yarl.interface.color.RGB](red=176, green=196, blue=222) |
| lightsteelblue1 | [RGB][yarl.interface.color.RGB](red=202, green=225, blue=255) |
| lightsteelblue2 | [RGB][yarl.interface.color.RGB](red=188, green=210, blue=238) |
| lightsteelblue3 | [RGB][yarl.interface.color.RGB](red=162, green=181, blue=205) |
| lightsteelblue4 | [RGB][yarl.interface.color.RGB](red=110, green=123, blue=139) |
| lightyellow1 | [RGB][yarl.interface.color.RGB](red=255, green=255, blue=224) |
| lightyellow2 | [RGB][yarl.interface.color.RGB](red=238, green=238, blue=209) |
| lightyellow3 | [RGB][yarl.interface.color.RGB](red=205, green=205, blue=180) |
| lightyellow4 | [RGB][yarl.interface.color.RGB](red=139, green=139, blue=122) |
| limegreen | [RGB][yarl.interface.color.RGB](red=50, green=205, blue=50) |
| linen | [RGB][yarl.interface.color.RGB](red=250, green=240, blue=230) |
| magenta | [RGB][yarl.interface.color.RGB](red=255, green=0, blue=255) |
| magenta2 | [RGB][yarl.interface.color.RGB](red=238, green=0, blue=238) |
| magenta3 | [RGB][yarl.interface.color.RGB](red=205, green=0, blue=205) |
| magenta4 | [RGB][yarl.interface.color.RGB](red=139, green=0, blue=139) |
| manganeseblue | [RGB][yarl.interface.color.RGB](red=3, green=168, blue=158) |
| maroon | [RGB][yarl.interface.color.RGB](red=128, green=0, blue=0) |
| maroon1 | [RGB][yarl.interface.color.RGB](red=255, green=52, blue=179) |
| maroon2 | [RGB][yarl.interface.color.RGB](red=238, green=48, blue=167) |
| maroon3 | [RGB][yarl.interface.color.RGB](red=205, green=41, blue=144) |
| maroon4 | [RGB][yarl.interface.color.RGB](red=139, green=28, blue=98) |
| mediumorchid | [RGB][yarl.interface.color.RGB](red=186, green=85, blue=211) |
| mediumorchid1 | [RGB][yarl.interface.color.RGB](red=224, green=102, blue=255) |
| mediumorchid2 | [RGB][yarl.interface.color.RGB](red=209, green=95, blue=238) |
| mediumorchid3 | [RGB][yarl.interface.color.RGB](red=180, green=82, blue=205) |
| mediumorchid4 | [RGB][yarl.interface.color.RGB](red=122, green=55, blue=139) |
| mediumpurple | [RGB][yarl.interface.color.RGB](red=147, green=112, blue=219) |
| mediumpurple1 | [RGB][yarl.interface.color.RGB](red=171, green=130, blue=255) |
| mediumpurple2 | [RGB][yarl.interface.color.RGB](red=159, green=121, blue=238) |
| mediumpurple3 | [RGB][yarl.interface.color.RGB](red=137, green=104, blue=205) |
| mediumpurple4 | [RGB][yarl.interface.color.RGB](red=93, green=71, blue=139) |
| mediumseagreen | [RGB][yarl.interface.color.RGB](red=60, green=179, blue=113) |
| mediumslateblue | [RGB][yarl.interface.color.RGB](red=123, green=104, blue=238) |
| mediumspringgreen | [RGB][yarl.interface.color.RGB](red=0, green=250, blue=154) |
| mediumturquoise | [RGB][yarl.interface.color.RGB](red=72, green=209, blue=204) |
| mediumvioletred | [RGB][yarl.interface.color.RGB](red=199, green=21, blue=133) |
| melon | [RGB][yarl.interface.color.RGB](red=227, green=168, blue=105) |
| midnightblue | [RGB][yarl.interface.color.RGB](red=25, green=25, blue=112) |
| mint | [RGB][yarl.interface.color.RGB](red=189, green=252, blue=201) |
| mintcream | [RGB][yarl.interface.color.RGB](red=245, green=255, blue=250) |
| mistyrose1 | [RGB][yarl.interface.color.RGB](red=255, green=228, blue=225) |
| mistyrose2 | [RGB][yarl.interface.color.RGB](red=238, green=213, blue=210) |
| mistyrose3 | [RGB][yarl.interface.color.RGB](red=205, green=183, blue=181) |
| mistyrose4 | [RGB][yarl.interface.color.RGB](red=139, green=125, blue=123) |
| moccasin | [RGB][yarl.interface.color.RGB](red=255, green=228, blue=181) |
| navajowhite1 | [RGB][yarl.interface.color.RGB](red=255, green=222, blue=173) |
| navajowhite2 | [RGB][yarl.interface.color.RGB](red=238, green=207, blue=161) |
| navajowhite3 | [RGB][yarl.interface.color.RGB](red=205, green=179, blue=139) |
| navajowhite4 | [RGB][yarl.interface.color.RGB](red=139, green=121, blue=94) |
| navy | [RGB][yarl.interface.color.RGB](red=0, green=0, blue=128) |
| oldlace | [RGB][yarl.interface.color.RGB](red=253, green=245, blue=230) |
| olive | [RGB][yarl.interface.color.RGB](red=128, green=128, blue=0) |
| olivedrab | [RGB][yarl.interface.color.RGB](red=107, green=142, blue=35) |
| olivedrab1 | [RGB][yarl.interface.color.RGB](red=192, green=255, blue=62) |
| olivedrab2 | [RGB][yarl.interface.color.RGB](red=179, green=238, blue=58) |
| olivedrab3 | [RGB][yarl.interface.color.RGB](red=154, green=205, blue=50) |
| olivedrab4 | [RGB][yarl.interface.color.RGB](red=105, green=139, blue=34) |
| orange | [RGB][yarl.interface.color.RGB](red=255, green=128, blue=0) |
| orange1 | [RGB][yarl.interface.color.RGB](red=255, green=165, blue=0) |
| orange2 | [RGB][yarl.interface.color.RGB](red=238, green=154, blue=0) |
| orange3 | [RGB][yarl.interface.color.RGB](red=205, green=133, blue=0) |
| orange4 | [RGB][yarl.interface.color.RGB](red=139, green=90, blue=0) |
| orangered1 | [RGB][yarl.interface.color.RGB](red=255, green=69, blue=0) |
| orangered2 | [RGB][yarl.interface.color.RGB](red=238, green=64, blue=0) |
| orangered3 | [RGB][yarl.interface.color.RGB](red=205, green=55, blue=0) |
| orangered4 | [RGB][yarl.interface.color.RGB](red=139, green=37, blue=0) |
| orchid | [RGB][yarl.interface.color.RGB](red=218, green=112, blue=214) |
| orchid1 | [RGB][yarl.interface.color.RGB](red=255, green=131, blue=250) |
| orchid2 | [RGB][yarl.interface.color.RGB](red=238, green=122, blue=233) |
| orchid3 | [RGB][yarl.interface.color.RGB](red=205, green=105, blue=201) |
| orchid4 | [RGB][yarl.interface.color.RGB](red=139, green=71, blue=137) |
| palegoldenrod | [RGB][yarl.interface.color.RGB](red=238, green=232, blue=170) |
| palegreen | [RGB][yarl.interface.color.RGB](red=152, green=251, blue=152) |
| palegreen1 | [RGB][yarl.interface.color.RGB](red=154, green=255, blue=154) |
| palegreen2 | [RGB][yarl.interface.color.RGB](red=144, green=238, blue=144) |
| palegreen3 | [RGB][yarl.interface.color.RGB](red=124, green=205, blue=124) |
| palegreen4 | [RGB][yarl.interface.color.RGB](red=84, green=139, blue=84) |
| paleturquoise1 | [RGB][yarl.interface.color.RGB](red=187, green=255, blue=255) |
| paleturquoise2 | [RGB][yarl.interface.color.RGB](red=174, green=238, blue=238) |
| paleturquoise3 | [RGB][yarl.interface.color.RGB](red=150, green=205, blue=205) |
| paleturquoise4 | [RGB][yarl.interface.color.RGB](red=102, green=139, blue=139) |
| palevioletred | [RGB][yarl.interface.color.RGB](red=219, green=112, blue=147) |
| palevioletred1 | [RGB][yarl.interface.color.RGB](red=255, green=130, blue=171) |
| palevioletred2 | [RGB][yarl.interface.color.RGB](red=238, green=121, blue=159) |
| palevioletred3 | [RGB][yarl.interface.color.RGB](red=205, green=104, blue=137) |
| palevioletred4 | [RGB][yarl.interface.color.RGB](red=139, green=71, blue=93) |
| papayawhip | [RGB][yarl.interface.color.RGB](red=255, green=239, blue=213) |
| peachpuff1 | [RGB][yarl.interface.color.RGB](red=255, green=218, blue=185) |
| peachpuff2 | [RGB][yarl.interface.color.RGB](red=238, green=203, blue=173) |
| peachpuff3 | [RGB][yarl.interface.color.RGB](red=205, green=175, blue=149) |
| peachpuff4 | [RGB][yarl.interface.color.RGB](red=139, green=119, blue=101) |
| peacock | [RGB][yarl.interface.color.RGB](red=51, green=161, blue=201) |
| pink | [RGB][yarl.interface.color.RGB](red=255, green=192, blue=203) |
| pink1 | [RGB][yarl.interface.color.RGB](red=255, green=181, blue=197) |
| pink2 | [RGB][yarl.interface.color.RGB](red=238, green=169, blue=184) |
| pink3 | [RGB][yarl.interface.color.RGB](red=205, green=145, blue=158) |
| pink4 | [RGB][yarl.interface.color.RGB](red=139, green=99, blue=108) |
| plum | [RGB][yarl.interface.color.RGB](red=221, green=160, blue=221) |
| plum1 | [RGB][yarl.interface.color.RGB](red=255, green=187, blue=255) |
| plum2 | [RGB][yarl.interface.color.RGB](red=238, green=174, blue=238) |
| plum3 | [RGB][yarl.interface.color.RGB](red=205, green=150, blue=205) |
| plum4 | [RGB][yarl.interface.color.RGB](red=139, green=102, blue=139) |
| powderblue | [RGB][yarl.interface.color.RGB](red=176, green=224, blue=230) |
| purple | [RGB][yarl.interface.color.RGB](red=128, green=0, blue=128) |
| purple1 | [RGB][yarl.interface.color.RGB](red=155, green=48, blue=255) |
| purple2 | [RGB][yarl.interface.color.RGB](red=145, green=44, blue=238) |
| purple3 | [RGB][yarl.interface.color.RGB](red=125, green=38, blue=205) |
| purple4 | [RGB][yarl.interface.color.RGB](red=85, green=26, blue=139) |
| raspberry | [RGB][yarl.interface.color.RGB](red=135, green=38, blue=87) |
| rawsienna | [RGB][yarl.interface.color.RGB](red=199, green=97, blue=20) |
| red1 | [RGB][yarl.interface.color.RGB](red=255, green=0, blue=0) |
| red2 | [RGB][yarl.interface.color.RGB](red=238, green=0, blue=0) |
| red3 | [RGB][yarl.interface.color.RGB](red=205, green=0, blue=0) |
| red4 | [RGB][yarl.interface.color.RGB](red=139, green=0, blue=0) |
| rosybrown | [RGB][yarl.interface.color.RGB](red=188, green=143, blue=143) |
| rosybrown1 | [RGB][yarl.interface.color.RGB](red=255, green=193, blue=193) |
| rosybrown2 | [RGB][yarl.interface.color.RGB](red=238, green=180, blue=180) |
| rosybrown3 | [RGB][yarl.interface.color.RGB](red=205, green=155, blue=155) |
| rosybrown4 | [RGB][yarl.interface.color.RGB](red=139, green=105, blue=105) |
| royalblue | [RGB][yarl.interface.color.RGB](red=65, green=105, blue=225) |
| royalblue1 | [RGB][yarl.interface.color.RGB](red=72, green=118, blue=255) |
| royalblue2 | [RGB][yarl.interface.color.RGB](red=67, green=110, blue=238) |
| royalblue3 | [RGB][yarl.interface.color.RGB](red=58, green=95, blue=205) |
| royalblue4 | [RGB][yarl.interface.color.RGB](red=39, green=64, blue=139) |
| salmon | [RGB][yarl.interface.color.RGB](red=250, green=128, blue=114) |
| salmon1 | [RGB][yarl.interface.color.RGB](red=255, green=140, blue=105) |
| salmon2 | [RGB][yarl.interface.color.RGB](red=238, green=130, blue=98) |
| salmon3 | [RGB][yarl.interface.color.RGB](red=205, green=112, blue=84) |
| salmon4 | [RGB][yarl.interface.color.RGB](red=139, green=76, blue=57) |
| sandybrown | [RGB][yarl.interface.color.RGB](red=244, green=164, blue=96) |
| sapgreen | [RGB][yarl.interface.color.RGB](red=48, green=128, blue=20) |
| seagreen1 | [RGB][yarl.interface.color.RGB](red=84, green=255, blue=159) |
| seagreen2 | [RGB][yarl.interface.color.RGB](red=78, green=238, blue=148) |
| seagreen3 | [RGB][yarl.interface.color.RGB](red=67, green=205, blue=128) |
| seagreen4 | [RGB][yarl.interface.color.RGB](red=46, green=139, blue=87) |
| seashell1 | [RGB][yarl.interface.color.RGB](red=255, green=245, blue=238) |
| seashell2 | [RGB][yarl.interface.color.RGB](red=238, green=229, blue=222) |
| seashell3 | [RGB][yarl.interface.color.RGB](red=205, green=197, blue=191) |
| seashell4 | [RGB][yarl.interface.color.RGB](red=139, green=134, blue=130) |
| sepia | [RGB][yarl.interface.color.RGB](red=94, green=38, blue=18) |
| sgibeet | [RGB][yarl.interface.color.RGB](red=142, green=56, blue=142) |
| sgibrightgray | [RGB][yarl.interface.color.RGB](red=197, green=193, blue=170) |
| sgichartreuse | [RGB][yarl.interface.color.RGB](red=113, green=198, blue=113) |
| sgidarkgray | [RGB][yarl.interface.color.RGB](red=85, green=85, blue=85) |
| sgigray12 | [RGB][yarl.interface.color.RGB](red=30, green=30, blue=30) |
| sgigray16 | [RGB][yarl.interface.color.RGB](red=40, green=40, blue=40) |
| sgigray32 | [RGB][yarl.interface.color.RGB](red=81, green=81, blue=81) |
| sgigray36 | [RGB][yarl.interface.color.RGB](red=91, green=91, blue=91) |
| sgigray52 | [RGB][yarl.interface.color.RGB](red=132, green=132, blue=132) |
| sgigray56 | [RGB][yarl.interface.color.RGB](red=142, green=142, blue=142) |
| sgigray72 | [RGB][yarl.interface.color.RGB](red=183, green=183, blue=183) |
| sgigray76 | [RGB][yarl.interface.color.RGB](red=193, green=193, blue=193) |
| sgigray92 | [RGB][yarl.interface.color.RGB](red=234, green=234, blue=234) |
| sgigray96 | [RGB][yarl.interface.color.RGB](red=244, green=244, blue=244) |
| sgilightblue | [RGB][yarl.interface.color.RGB](red=125, green=158, blue=192) |
| sgilightgray | [RGB][yarl.interface.color.RGB](red=170, green=170, blue=170) |
| sgiolivedrab | [RGB][yarl.interface.color.RGB](red=142, green=142, blue=56) |
| sgisalmon | [RGB][yarl.interface.color.RGB](red=198, green=113, blue=113) |
| sgislateblue | [RGB][yarl.interface.color.RGB](red=113, green=113, blue=198) |
| sgiteal | [RGB][yarl.interface.color.RGB](red=56, green=142, blue=142) |
| sienna | [RGB][yarl.interface.color.RGB](red=160, green=82, blue=45) |
| sienna1 | [RGB][yarl.interface.color.RGB](red=255, green=130, blue=71) |
| sienna2 | [RGB][yarl.interface.color.RGB](red=238, green=121, blue=66) |
| sienna3 | [RGB][yarl.interface.color.RGB](red=205, green=104, blue=57) |
| sienna4 | [RGB][yarl.interface.color.RGB](red=139, green=71, blue=38) |
| silver | [RGB][yarl.interface.color.RGB](red=192, green=192, blue=192) |
| skyblue | [RGB][yarl.interface.color.RGB](red=135, green=206, blue=235) |
| skyblue1 | [RGB][yarl.interface.color.RGB](red=135, green=206, blue=255) |
| skyblue2 | [RGB][yarl.interface.color.RGB](red=126, green=192, blue=238) |
| skyblue3 | [RGB][yarl.interface.color.RGB](red=108, green=166, blue=205) |
| skyblue4 | [RGB][yarl.interface.color.RGB](red=74, green=112, blue=139) |
| slateblue | [RGB][yarl.interface.color.RGB](red=106, green=90, blue=205) |
| slateblue1 | [RGB][yarl.interface.color.RGB](red=131, green=111, blue=255) |
| slateblue2 | [RGB][yarl.interface.color.RGB](red=122, green=103, blue=238) |
| slateblue3 | [RGB][yarl.interface.color.RGB](red=105, green=89, blue=205) |
| slateblue4 | [RGB][yarl.interface.color.RGB](red=71, green=60, blue=139) |
| slategray | [RGB][yarl.interface.color.RGB](red=112, green=128, blue=144) |
| slategray1 | [RGB][yarl.interface.color.RGB](red=198, green=226, blue=255) |
| slategray2 | [RGB][yarl.interface.color.RGB](red=185, green=211, blue=238) |
| slategray3 | [RGB][yarl.interface.color.RGB](red=159, green=182, blue=205) |
| slategray4 | [RGB][yarl.interface.color.RGB](red=108, green=123, blue=139) |
| snow1 | [RGB][yarl.interface.color.RGB](red=255, green=250, blue=250) |
| snow2 | [RGB][yarl.interface.color.RGB](red=238, green=233, blue=233) |
| snow3 | [RGB][yarl.interface.color.RGB](red=205, green=201, blue=201) |
| snow4 | [RGB][yarl.interface.color.RGB](red=139, green=137, blue=137) |
| springgreen | [RGB][yarl.interface.color.RGB](red=0, green=255, blue=127) |
| springgreen1 | [RGB][yarl.interface.color.RGB](red=0, green=238, blue=118) |
| springgreen2 | [RGB][yarl.interface.color.RGB](red=0, green=205, blue=102) |
| springgreen3 | [RGB][yarl.interface.color.RGB](red=0, green=139, blue=69) |
| steelblue | [RGB][yarl.interface.color.RGB](red=70, green=130, blue=180) |
| steelblue1 | [RGB][yarl.interface.color.RGB](red=99, green=184, blue=255) |
| steelblue2 | [RGB][yarl.interface.color.RGB](red=92, green=172, blue=238) |
| steelblue3 | [RGB][yarl.interface.color.RGB](red=79, green=148, blue=205) |
| steelblue4 | [RGB][yarl.interface.color.RGB](red=54, green=100, blue=139) |
| tan | [RGB][yarl.interface.color.RGB](red=210, green=180, blue=140) |
| tan1 | [RGB][yarl.interface.color.RGB](red=255, green=165, blue=79) |
| tan2 | [RGB][yarl.interface.color.RGB](red=238, green=154, blue=73) |
| tan3 | [RGB][yarl.interface.color.RGB](red=205, green=133, blue=63) |
| tan4 | [RGB][yarl.interface.color.RGB](red=139, green=90, blue=43) |
| teal | [RGB][yarl.interface.color.RGB](red=0, green=128, blue=128) |
| thistle | [RGB][yarl.interface.color.RGB](red=216, green=191, blue=216) |
| thistle1 | [RGB][yarl.interface.color.RGB](red=255, green=225, blue=255) |
| thistle2 | [RGB][yarl.interface.color.RGB](red=238, green=210, blue=238) |
| thistle3 | [RGB][yarl.interface.color.RGB](red=205, green=181, blue=205) |
| thistle4 | [RGB][yarl.interface.color.RGB](red=139, green=123, blue=139) |
| tomato1 | [RGB][yarl.interface.color.RGB](red=255, green=99, blue=71) |
| tomato2 | [RGB][yarl.interface.color.RGB](red=238, green=92, blue=66) |
| tomato3 | [RGB][yarl.interface.color.RGB](red=205, green=79, blue=57) |
| tomato4 | [RGB][yarl.interface.color.RGB](red=139, green=54, blue=38) |
| turquoise | [RGB][yarl.interface.color.RGB](red=64, green=224, blue=208) |
| turquoise1 | [RGB][yarl.interface.color.RGB](red=0, green=245, blue=255) |
| turquoise2 | [RGB][yarl.interface.color.RGB](red=0, green=229, blue=238) |
| turquoise3 | [RGB][yarl.interface.color.RGB](red=0, green=197, blue=205) |
| turquoise4 | [RGB][yarl.interface.color.RGB](red=0, green=134, blue=139) |
| turquoiseblue | [RGB][yarl.interface.color.RGB](red=0, green=199, blue=140) |
| violet | [RGB][yarl.interface.color.RGB](red=238, green=130, blue=238) |
| violetred | [RGB][yarl.interface.color.RGB](red=208, green=32, blue=144) |
| violetred1 | [RGB][yarl.interface.color.RGB](red=255, green=62, blue=150) |
| violetred2 | [RGB][yarl.interface.color.RGB](red=238, green=58, blue=140) |
| violetred3 | [RGB][yarl.interface.color.RGB](red=205, green=50, blue=120) |
| violetred4 | [RGB][yarl.interface.color.RGB](red=139, green=34, blue=82) |
| warmgrey | [RGB][yarl.interface.color.RGB](red=128, green=128, blue=105) |
| wheat | [RGB][yarl.interface.color.RGB](red=245, green=222, blue=179) |
| wheat1 | [RGB][yarl.interface.color.RGB](red=255, green=231, blue=186) |
| wheat2 | [RGB][yarl.interface.color.RGB](red=238, green=216, blue=174) |
| wheat3 | [RGB][yarl.interface.color.RGB](red=205, green=186, blue=150) |
| wheat4 | [RGB][yarl.interface.color.RGB](red=139, green=126, blue=102) |
| white1 | [RGB][yarl.interface.color.RGB](red=255, green=255, blue=255) |
| whitesmoke | [RGB][yarl.interface.color.RGB](red=245, green=245, blue=245) |
| yellow1 | [RGB][yarl.interface.color.RGB](red=255, green=255, blue=0) |
| yellow2 | [RGB][yarl.interface.color.RGB](red=238, green=238, blue=0) |
| yellow3 | [RGB][yarl.interface.color.RGB](red=205, green=205, blue=0) |
| yellow4 | [RGB][yarl.interface.color.RGB](red=139, green=139, blue=0) |
"""

from collections import OrderedDict, namedtuple
from enum import Enum
from typing import NamedTuple


class RGB(NamedTuple):
    """NamedTuple to represent an RGB color."""

    red: int
    """Red component of the color."""

    green: int
    """Green component of the color."""

    blue: int
    """Blue component of the color."""

    def hex_format(self) -> str:
        """Method to obtain the color in hex format.

        Returns:
            Color as a `#<ab><cd><de>` hex string.
        """
        return f"#{self.red:02X}{self.green:02X}{self.blue:02X}"


# Color Contants
class ColorConstants(Enum):
    """Enum of all the colors.

    If the name of a color is `xyz` in the above table,
    it's corresponding enum is `XYZ`. For example,
    `white1` is `ColorConstants.WHITE1`.
    """

    ALICEBLUE = RGB(240, 248, 255)

    ANTIQUEWHITE = RGB(250, 235, 215)

    ANTIQUEWHITE1 = RGB(255, 239, 219)

    ANTIQUEWHITE2 = RGB(238, 223, 204)

    ANTIQUEWHITE3 = RGB(205, 192, 176)

    ANTIQUEWHITE4 = RGB(139, 131, 120)

    AQUA = RGB(0, 255, 255)

    AQUAMARINE1 = RGB(127, 255, 212)

    AQUAMARINE2 = RGB(118, 238, 198)

    AQUAMARINE3 = RGB(102, 205, 170)

    AQUAMARINE4 = RGB(69, 139, 116)

    AZURE1 = RGB(240, 255, 255)

    AZURE2 = RGB(224, 238, 238)

    AZURE3 = RGB(193, 205, 205)

    AZURE4 = RGB(131, 139, 139)

    BANANA = RGB(227, 207, 87)

    BEIGE = RGB(245, 245, 220)

    BISQUE1 = RGB(255, 228, 196)

    BISQUE2 = RGB(238, 213, 183)

    BISQUE3 = RGB(205, 183, 158)

    BISQUE4 = RGB(139, 125, 107)

    BLACK = RGB(0, 0, 0)

    BLANCHEDALMOND = RGB(255, 235, 205)

    BLUE = RGB(0, 0, 255)

    BLUE2 = RGB(0, 0, 238)

    BLUE3 = RGB(0, 0, 205)

    BLUE4 = RGB(0, 0, 139)

    BLUEVIOLET = RGB(138, 43, 226)

    BRICK = RGB(156, 102, 31)

    BROWN = RGB(165, 42, 42)

    BROWN1 = RGB(255, 64, 64)

    BROWN2 = RGB(238, 59, 59)

    BROWN3 = RGB(205, 51, 51)

    BROWN4 = RGB(139, 35, 35)

    BURLYWOOD = RGB(222, 184, 135)

    BURLYWOOD1 = RGB(255, 211, 155)

    BURLYWOOD2 = RGB(238, 197, 145)

    BURLYWOOD3 = RGB(205, 170, 125)

    BURLYWOOD4 = RGB(139, 115, 85)

    BURNTSIENNA = RGB(138, 54, 15)

    BURNTUMBER = RGB(138, 51, 36)

    CADETBLUE = RGB(95, 158, 160)

    CADETBLUE1 = RGB(152, 245, 255)

    CADETBLUE2 = RGB(142, 229, 238)

    CADETBLUE3 = RGB(122, 197, 205)

    CADETBLUE4 = RGB(83, 134, 139)

    CADMIUMORANGE = RGB(255, 97, 3)

    CADMIUMYELLOW = RGB(255, 153, 18)

    CARROT = RGB(237, 145, 33)

    CHARTREUSE1 = RGB(127, 255, 0)

    CHARTREUSE2 = RGB(118, 238, 0)

    CHARTREUSE3 = RGB(102, 205, 0)

    CHARTREUSE4 = RGB(69, 139, 0)

    CHOCOLATE = RGB(210, 105, 30)

    CHOCOLATE1 = RGB(255, 127, 36)

    CHOCOLATE2 = RGB(238, 118, 33)

    CHOCOLATE3 = RGB(205, 102, 29)

    CHOCOLATE4 = RGB(139, 69, 19)

    COBALT = RGB(61, 89, 171)

    COBALTGREEN = RGB(61, 145, 64)

    COLDGREY = RGB(128, 138, 135)

    CORAL = RGB(255, 127, 80)

    CORAL1 = RGB(255, 114, 86)

    CORAL2 = RGB(238, 106, 80)

    CORAL3 = RGB(205, 91, 69)

    CORAL4 = RGB(139, 62, 47)

    CORNFLOWERBLUE = RGB(100, 149, 237)

    CORNSILK1 = RGB(255, 248, 220)

    CORNSILK2 = RGB(238, 232, 205)

    CORNSILK3 = RGB(205, 200, 177)

    CORNSILK4 = RGB(139, 136, 120)

    CRIMSON = RGB(220, 20, 60)

    CYAN2 = RGB(0, 238, 238)

    CYAN3 = RGB(0, 205, 205)

    CYAN4 = RGB(0, 139, 139)

    DARKGOLDENROD = RGB(184, 134, 11)

    DARKGOLDENROD1 = RGB(255, 185, 15)

    DARKGOLDENROD2 = RGB(238, 173, 14)

    DARKGOLDENROD3 = RGB(205, 149, 12)

    DARKGOLDENROD4 = RGB(139, 101, 8)

    DARKGRAY = RGB(169, 169, 169)

    DARKGREEN = RGB(0, 100, 0)

    DARKKHAKI = RGB(189, 183, 107)

    DARKOLIVEGREEN = RGB(85, 107, 47)

    DARKOLIVEGREEN1 = RGB(202, 255, 112)

    DARKOLIVEGREEN2 = RGB(188, 238, 104)

    DARKOLIVEGREEN3 = RGB(162, 205, 90)

    DARKOLIVEGREEN4 = RGB(110, 139, 61)

    DARKORANGE = RGB(255, 140, 0)

    DARKORANGE1 = RGB(255, 127, 0)

    DARKORANGE2 = RGB(238, 118, 0)

    DARKORANGE3 = RGB(205, 102, 0)

    DARKORANGE4 = RGB(139, 69, 0)

    DARKORCHID = RGB(153, 50, 204)

    DARKORCHID1 = RGB(191, 62, 255)

    DARKORCHID2 = RGB(178, 58, 238)

    DARKORCHID3 = RGB(154, 50, 205)

    DARKORCHID4 = RGB(104, 34, 139)

    DARKSALMON = RGB(233, 150, 122)

    DARKSEAGREEN = RGB(143, 188, 143)

    DARKSEAGREEN1 = RGB(193, 255, 193)

    DARKSEAGREEN2 = RGB(180, 238, 180)

    DARKSEAGREEN3 = RGB(155, 205, 155)

    DARKSEAGREEN4 = RGB(105, 139, 105)

    DARKSLATEBLUE = RGB(72, 61, 139)

    DARKSLATEGRAY = RGB(47, 79, 79)

    DARKSLATEGRAY1 = RGB(151, 255, 255)

    DARKSLATEGRAY2 = RGB(141, 238, 238)

    DARKSLATEGRAY3 = RGB(121, 205, 205)

    DARKSLATEGRAY4 = RGB(82, 139, 139)

    DARKTURQUOISE = RGB(0, 206, 209)

    DARKVIOLET = RGB(148, 0, 211)

    DEEPPINK1 = RGB(255, 20, 147)

    DEEPPINK2 = RGB(238, 18, 137)

    DEEPPINK3 = RGB(205, 16, 118)

    DEEPPINK4 = RGB(139, 10, 80)

    DEEPSKYBLUE1 = RGB(0, 191, 255)

    DEEPSKYBLUE2 = RGB(0, 178, 238)

    DEEPSKYBLUE3 = RGB(0, 154, 205)

    DEEPSKYBLUE4 = RGB(0, 104, 139)

    DIMGRAY = RGB(105, 105, 105)

    DODGERBLUE1 = RGB(30, 144, 255)

    DODGERBLUE2 = RGB(28, 134, 238)

    DODGERBLUE3 = RGB(24, 116, 205)

    DODGERBLUE4 = RGB(16, 78, 139)

    EGGSHELL = RGB(252, 230, 201)

    EMERALDGREEN = RGB(0, 201, 87)

    FIREBRICK = RGB(178, 34, 34)

    FIREBRICK1 = RGB(255, 48, 48)

    FIREBRICK2 = RGB(238, 44, 44)

    FIREBRICK3 = RGB(205, 38, 38)

    FIREBRICK4 = RGB(139, 26, 26)

    FLESH = RGB(255, 125, 64)

    FLORALWHITE = RGB(255, 250, 240)

    FORESTGREEN = RGB(34, 139, 34)

    GAINSBORO = RGB(220, 220, 220)

    GHOSTWHITE = RGB(248, 248, 255)

    GOLD1 = RGB(255, 215, 0)

    GOLD2 = RGB(238, 201, 0)

    GOLD3 = RGB(205, 173, 0)

    GOLD4 = RGB(139, 117, 0)

    GOLDENROD = RGB(218, 165, 32)

    GOLDENROD1 = RGB(255, 193, 37)

    GOLDENROD2 = RGB(238, 180, 34)

    GOLDENROD3 = RGB(205, 155, 29)

    GOLDENROD4 = RGB(139, 105, 20)

    GRAY = RGB(128, 128, 128)

    GRAY1 = RGB(3, 3, 3)

    GRAY10 = RGB(26, 26, 26)

    GRAY11 = RGB(28, 28, 28)

    GRAY12 = RGB(31, 31, 31)

    GRAY13 = RGB(33, 33, 33)

    GRAY14 = RGB(36, 36, 36)

    GRAY15 = RGB(38, 38, 38)

    GRAY16 = RGB(41, 41, 41)

    GRAY17 = RGB(43, 43, 43)

    GRAY18 = RGB(46, 46, 46)

    GRAY19 = RGB(48, 48, 48)

    GRAY2 = RGB(5, 5, 5)

    GRAY20 = RGB(51, 51, 51)

    GRAY21 = RGB(54, 54, 54)

    GRAY22 = RGB(56, 56, 56)

    GRAY23 = RGB(59, 59, 59)

    GRAY24 = RGB(61, 61, 61)

    GRAY25 = RGB(64, 64, 64)

    GRAY26 = RGB(66, 66, 66)

    GRAY27 = RGB(69, 69, 69)

    GRAY28 = RGB(71, 71, 71)

    GRAY29 = RGB(74, 74, 74)

    GRAY3 = RGB(8, 8, 8)

    GRAY30 = RGB(77, 77, 77)

    GRAY31 = RGB(79, 79, 79)

    GRAY32 = RGB(82, 82, 82)

    GRAY33 = RGB(84, 84, 84)

    GRAY34 = RGB(87, 87, 87)

    GRAY35 = RGB(89, 89, 89)

    GRAY36 = RGB(92, 92, 92)

    GRAY37 = RGB(94, 94, 94)

    GRAY38 = RGB(97, 97, 97)

    GRAY39 = RGB(99, 99, 99)

    GRAY4 = RGB(10, 10, 10)

    GRAY40 = RGB(102, 102, 102)

    GRAY42 = RGB(107, 107, 107)

    GRAY43 = RGB(110, 110, 110)

    GRAY44 = RGB(112, 112, 112)

    GRAY45 = RGB(115, 115, 115)

    GRAY46 = RGB(117, 117, 117)

    GRAY47 = RGB(120, 120, 120)

    GRAY48 = RGB(122, 122, 122)

    GRAY49 = RGB(125, 125, 125)

    GRAY5 = RGB(13, 13, 13)

    GRAY50 = RGB(127, 127, 127)

    GRAY51 = RGB(130, 130, 130)

    GRAY52 = RGB(133, 133, 133)

    GRAY53 = RGB(135, 135, 135)

    GRAY54 = RGB(138, 138, 138)

    GRAY55 = RGB(140, 140, 140)

    GRAY56 = RGB(143, 143, 143)

    GRAY57 = RGB(145, 145, 145)

    GRAY58 = RGB(148, 148, 148)

    GRAY59 = RGB(150, 150, 150)

    GRAY6 = RGB(15, 15, 15)

    GRAY60 = RGB(153, 153, 153)

    GRAY61 = RGB(156, 156, 156)

    GRAY62 = RGB(158, 158, 158)

    GRAY63 = RGB(161, 161, 161)

    GRAY64 = RGB(163, 163, 163)

    GRAY65 = RGB(166, 166, 166)

    GRAY66 = RGB(168, 168, 168)

    GRAY67 = RGB(171, 171, 171)

    GRAY68 = RGB(173, 173, 173)

    GRAY69 = RGB(176, 176, 176)

    GRAY7 = RGB(18, 18, 18)

    GRAY70 = RGB(179, 179, 179)

    GRAY71 = RGB(181, 181, 181)

    GRAY72 = RGB(184, 184, 184)

    GRAY73 = RGB(186, 186, 186)

    GRAY74 = RGB(189, 189, 189)

    GRAY75 = RGB(191, 191, 191)

    GRAY76 = RGB(194, 194, 194)

    GRAY77 = RGB(196, 196, 196)

    GRAY78 = RGB(199, 199, 199)

    GRAY79 = RGB(201, 201, 201)

    GRAY8 = RGB(20, 20, 20)

    GRAY80 = RGB(204, 204, 204)

    GRAY81 = RGB(207, 207, 207)

    GRAY82 = RGB(209, 209, 209)

    GRAY83 = RGB(212, 212, 212)

    GRAY84 = RGB(214, 214, 214)

    GRAY85 = RGB(217, 217, 217)

    GRAY86 = RGB(219, 219, 219)

    GRAY87 = RGB(222, 222, 222)

    GRAY88 = RGB(224, 224, 224)

    GRAY89 = RGB(227, 227, 227)

    GRAY9 = RGB(23, 23, 23)

    GRAY90 = RGB(229, 229, 229)

    GRAY91 = RGB(232, 232, 232)

    GRAY92 = RGB(235, 235, 235)

    GRAY93 = RGB(237, 237, 237)

    GRAY94 = RGB(240, 240, 240)

    GRAY95 = RGB(242, 242, 242)

    GRAY97 = RGB(247, 247, 247)

    GRAY98 = RGB(250, 250, 250)

    GRAY99 = RGB(252, 252, 252)

    GREEN = RGB(0, 128, 0)

    GREEN1 = RGB(0, 255, 0)

    GREEN2 = RGB(0, 238, 0)

    GREEN3 = RGB(0, 205, 0)

    GREEN4 = RGB(0, 139, 0)

    GREENYELLOW = RGB(173, 255, 47)

    HONEYDEW1 = RGB(240, 255, 240)

    HONEYDEW2 = RGB(224, 238, 224)

    HONEYDEW3 = RGB(193, 205, 193)

    HONEYDEW4 = RGB(131, 139, 131)

    HOTPINK = RGB(255, 105, 180)

    HOTPINK1 = RGB(255, 110, 180)

    HOTPINK2 = RGB(238, 106, 167)

    HOTPINK3 = RGB(205, 96, 144)

    HOTPINK4 = RGB(139, 58, 98)

    INDIANRED = RGB(205, 92, 92)

    INDIANRED1 = RGB(255, 106, 106)

    INDIANRED2 = RGB(238, 99, 99)

    INDIANRED3 = RGB(205, 85, 85)

    INDIANRED4 = RGB(139, 58, 58)

    INDIGO = RGB(75, 0, 130)

    IVORY1 = RGB(255, 255, 240)

    IVORY2 = RGB(238, 238, 224)

    IVORY3 = RGB(205, 205, 193)

    IVORY4 = RGB(139, 139, 131)

    IVORYBLACK = RGB(41, 36, 33)

    KHAKI = RGB(240, 230, 140)

    KHAKI1 = RGB(255, 246, 143)

    KHAKI2 = RGB(238, 230, 133)

    KHAKI3 = RGB(205, 198, 115)

    KHAKI4 = RGB(139, 134, 78)

    LAVENDER = RGB(230, 230, 250)

    LAVENDERBLUSH1 = RGB(255, 240, 245)

    LAVENDERBLUSH2 = RGB(238, 224, 229)

    LAVENDERBLUSH3 = RGB(205, 193, 197)

    LAVENDERBLUSH4 = RGB(139, 131, 134)

    LAWNGREEN = RGB(124, 252, 0)

    LEMONCHIFFON1 = RGB(255, 250, 205)

    LEMONCHIFFON2 = RGB(238, 233, 191)

    LEMONCHIFFON3 = RGB(205, 201, 165)

    LEMONCHIFFON4 = RGB(139, 137, 112)

    LIGHTBLUE = RGB(173, 216, 230)

    LIGHTBLUE1 = RGB(191, 239, 255)

    LIGHTBLUE2 = RGB(178, 223, 238)

    LIGHTBLUE3 = RGB(154, 192, 205)

    LIGHTBLUE4 = RGB(104, 131, 139)

    LIGHTCORAL = RGB(240, 128, 128)

    LIGHTCYAN1 = RGB(224, 255, 255)

    LIGHTCYAN2 = RGB(209, 238, 238)

    LIGHTCYAN3 = RGB(180, 205, 205)

    LIGHTCYAN4 = RGB(122, 139, 139)

    LIGHTGOLDENROD1 = RGB(255, 236, 139)

    LIGHTGOLDENROD2 = RGB(238, 220, 130)

    LIGHTGOLDENROD3 = RGB(205, 190, 112)

    LIGHTGOLDENROD4 = RGB(139, 129, 76)

    LIGHTGOLDENRODYELLOW = RGB(250, 250, 210)

    LIGHTGREY = RGB(211, 211, 211)

    LIGHTPINK = RGB(255, 182, 193)

    LIGHTPINK1 = RGB(255, 174, 185)

    LIGHTPINK2 = RGB(238, 162, 173)

    LIGHTPINK3 = RGB(205, 140, 149)

    LIGHTPINK4 = RGB(139, 95, 101)

    LIGHTSALMON1 = RGB(255, 160, 122)

    LIGHTSALMON2 = RGB(238, 149, 114)

    LIGHTSALMON3 = RGB(205, 129, 98)

    LIGHTSALMON4 = RGB(139, 87, 66)

    LIGHTSEAGREEN = RGB(32, 178, 170)

    LIGHTSKYBLUE = RGB(135, 206, 250)

    LIGHTSKYBLUE1 = RGB(176, 226, 255)

    LIGHTSKYBLUE2 = RGB(164, 211, 238)

    LIGHTSKYBLUE3 = RGB(141, 182, 205)

    LIGHTSKYBLUE4 = RGB(96, 123, 139)

    LIGHTSLATEBLUE = RGB(132, 112, 255)

    LIGHTSLATEGRAY = RGB(119, 136, 153)

    LIGHTSTEELBLUE = RGB(176, 196, 222)

    LIGHTSTEELBLUE1 = RGB(202, 225, 255)

    LIGHTSTEELBLUE2 = RGB(188, 210, 238)

    LIGHTSTEELBLUE3 = RGB(162, 181, 205)

    LIGHTSTEELBLUE4 = RGB(110, 123, 139)

    LIGHTYELLOW1 = RGB(255, 255, 224)

    LIGHTYELLOW2 = RGB(238, 238, 209)

    LIGHTYELLOW3 = RGB(205, 205, 180)

    LIGHTYELLOW4 = RGB(139, 139, 122)

    LIMEGREEN = RGB(50, 205, 50)

    LINEN = RGB(250, 240, 230)

    MAGENTA = RGB(255, 0, 255)

    MAGENTA2 = RGB(238, 0, 238)

    MAGENTA3 = RGB(205, 0, 205)

    MAGENTA4 = RGB(139, 0, 139)

    MANGANESEBLUE = RGB(3, 168, 158)

    MAROON = RGB(128, 0, 0)

    MAROON1 = RGB(255, 52, 179)

    MAROON2 = RGB(238, 48, 167)

    MAROON3 = RGB(205, 41, 144)

    MAROON4 = RGB(139, 28, 98)

    MEDIUMORCHID = RGB(186, 85, 211)

    MEDIUMORCHID1 = RGB(224, 102, 255)

    MEDIUMORCHID2 = RGB(209, 95, 238)

    MEDIUMORCHID3 = RGB(180, 82, 205)

    MEDIUMORCHID4 = RGB(122, 55, 139)

    MEDIUMPURPLE = RGB(147, 112, 219)

    MEDIUMPURPLE1 = RGB(171, 130, 255)

    MEDIUMPURPLE2 = RGB(159, 121, 238)

    MEDIUMPURPLE3 = RGB(137, 104, 205)

    MEDIUMPURPLE4 = RGB(93, 71, 139)

    MEDIUMSEAGREEN = RGB(60, 179, 113)

    MEDIUMSLATEBLUE = RGB(123, 104, 238)

    MEDIUMSPRINGGREEN = RGB(0, 250, 154)

    MEDIUMTURQUOISE = RGB(72, 209, 204)

    MEDIUMVIOLETRED = RGB(199, 21, 133)

    MELON = RGB(227, 168, 105)

    MIDNIGHTBLUE = RGB(25, 25, 112)

    MINT = RGB(189, 252, 201)

    MINTCREAM = RGB(245, 255, 250)

    MISTYROSE1 = RGB(255, 228, 225)

    MISTYROSE2 = RGB(238, 213, 210)

    MISTYROSE3 = RGB(205, 183, 181)

    MISTYROSE4 = RGB(139, 125, 123)

    MOCCASIN = RGB(255, 228, 181)

    NAVAJOWHITE1 = RGB(255, 222, 173)

    NAVAJOWHITE2 = RGB(238, 207, 161)

    NAVAJOWHITE3 = RGB(205, 179, 139)

    NAVAJOWHITE4 = RGB(139, 121, 94)

    NAVY = RGB(0, 0, 128)

    OLDLACE = RGB(253, 245, 230)

    OLIVE = RGB(128, 128, 0)

    OLIVEDRAB = RGB(107, 142, 35)

    OLIVEDRAB1 = RGB(192, 255, 62)

    OLIVEDRAB2 = RGB(179, 238, 58)

    OLIVEDRAB3 = RGB(154, 205, 50)

    OLIVEDRAB4 = RGB(105, 139, 34)

    ORANGE = RGB(255, 128, 0)

    ORANGE1 = RGB(255, 165, 0)

    ORANGE2 = RGB(238, 154, 0)

    ORANGE3 = RGB(205, 133, 0)

    ORANGE4 = RGB(139, 90, 0)

    ORANGERED1 = RGB(255, 69, 0)

    ORANGERED2 = RGB(238, 64, 0)

    ORANGERED3 = RGB(205, 55, 0)

    ORANGERED4 = RGB(139, 37, 0)

    ORCHID = RGB(218, 112, 214)

    ORCHID1 = RGB(255, 131, 250)

    ORCHID2 = RGB(238, 122, 233)

    ORCHID3 = RGB(205, 105, 201)

    ORCHID4 = RGB(139, 71, 137)

    PALEGOLDENROD = RGB(238, 232, 170)

    PALEGREEN = RGB(152, 251, 152)

    PALEGREEN1 = RGB(154, 255, 154)

    PALEGREEN2 = RGB(144, 238, 144)

    PALEGREEN3 = RGB(124, 205, 124)

    PALEGREEN4 = RGB(84, 139, 84)

    PALETURQUOISE1 = RGB(187, 255, 255)

    PALETURQUOISE2 = RGB(174, 238, 238)

    PALETURQUOISE3 = RGB(150, 205, 205)

    PALETURQUOISE4 = RGB(102, 139, 139)

    PALEVIOLETRED = RGB(219, 112, 147)

    PALEVIOLETRED1 = RGB(255, 130, 171)

    PALEVIOLETRED2 = RGB(238, 121, 159)

    PALEVIOLETRED3 = RGB(205, 104, 137)

    PALEVIOLETRED4 = RGB(139, 71, 93)

    PAPAYAWHIP = RGB(255, 239, 213)

    PEACHPUFF1 = RGB(255, 218, 185)

    PEACHPUFF2 = RGB(238, 203, 173)

    PEACHPUFF3 = RGB(205, 175, 149)

    PEACHPUFF4 = RGB(139, 119, 101)

    PEACOCK = RGB(51, 161, 201)

    PINK = RGB(255, 192, 203)

    PINK1 = RGB(255, 181, 197)

    PINK2 = RGB(238, 169, 184)

    PINK3 = RGB(205, 145, 158)

    PINK4 = RGB(139, 99, 108)

    PLUM = RGB(221, 160, 221)

    PLUM1 = RGB(255, 187, 255)

    PLUM2 = RGB(238, 174, 238)

    PLUM3 = RGB(205, 150, 205)

    PLUM4 = RGB(139, 102, 139)

    POWDERBLUE = RGB(176, 224, 230)

    PURPLE = RGB(128, 0, 128)

    PURPLE1 = RGB(155, 48, 255)

    PURPLE2 = RGB(145, 44, 238)

    PURPLE3 = RGB(125, 38, 205)

    PURPLE4 = RGB(85, 26, 139)

    RASPBERRY = RGB(135, 38, 87)

    RAWSIENNA = RGB(199, 97, 20)

    RED1 = RGB(255, 0, 0)

    RED2 = RGB(238, 0, 0)

    RED3 = RGB(205, 0, 0)

    RED4 = RGB(139, 0, 0)

    ROSYBROWN = RGB(188, 143, 143)

    ROSYBROWN1 = RGB(255, 193, 193)

    ROSYBROWN2 = RGB(238, 180, 180)

    ROSYBROWN3 = RGB(205, 155, 155)

    ROSYBROWN4 = RGB(139, 105, 105)

    ROYALBLUE = RGB(65, 105, 225)

    ROYALBLUE1 = RGB(72, 118, 255)

    ROYALBLUE2 = RGB(67, 110, 238)

    ROYALBLUE3 = RGB(58, 95, 205)

    ROYALBLUE4 = RGB(39, 64, 139)

    SALMON = RGB(250, 128, 114)

    SALMON1 = RGB(255, 140, 105)

    SALMON2 = RGB(238, 130, 98)

    SALMON3 = RGB(205, 112, 84)

    SALMON4 = RGB(139, 76, 57)

    SANDYBROWN = RGB(244, 164, 96)

    SAPGREEN = RGB(48, 128, 20)

    SEAGREEN1 = RGB(84, 255, 159)

    SEAGREEN2 = RGB(78, 238, 148)

    SEAGREEN3 = RGB(67, 205, 128)

    SEAGREEN4 = RGB(46, 139, 87)

    SEASHELL1 = RGB(255, 245, 238)

    SEASHELL2 = RGB(238, 229, 222)

    SEASHELL3 = RGB(205, 197, 191)

    SEASHELL4 = RGB(139, 134, 130)

    SEPIA = RGB(94, 38, 18)

    SGIBEET = RGB(142, 56, 142)

    SGIBRIGHTGRAY = RGB(197, 193, 170)

    SGICHARTREUSE = RGB(113, 198, 113)

    SGIDARKGRAY = RGB(85, 85, 85)

    SGIGRAY12 = RGB(30, 30, 30)

    SGIGRAY16 = RGB(40, 40, 40)

    SGIGRAY32 = RGB(81, 81, 81)

    SGIGRAY36 = RGB(91, 91, 91)

    SGIGRAY52 = RGB(132, 132, 132)

    SGIGRAY56 = RGB(142, 142, 142)

    SGIGRAY72 = RGB(183, 183, 183)

    SGIGRAY76 = RGB(193, 193, 193)

    SGIGRAY92 = RGB(234, 234, 234)

    SGIGRAY96 = RGB(244, 244, 244)

    SGILIGHTBLUE = RGB(125, 158, 192)

    SGILIGHTGRAY = RGB(170, 170, 170)

    SGIOLIVEDRAB = RGB(142, 142, 56)

    SGISALMON = RGB(198, 113, 113)

    SGISLATEBLUE = RGB(113, 113, 198)

    SGITEAL = RGB(56, 142, 142)

    SIENNA = RGB(160, 82, 45)

    SIENNA1 = RGB(255, 130, 71)

    SIENNA2 = RGB(238, 121, 66)

    SIENNA3 = RGB(205, 104, 57)

    SIENNA4 = RGB(139, 71, 38)

    SILVER = RGB(192, 192, 192)

    SKYBLUE = RGB(135, 206, 235)

    SKYBLUE1 = RGB(135, 206, 255)

    SKYBLUE2 = RGB(126, 192, 238)

    SKYBLUE3 = RGB(108, 166, 205)

    SKYBLUE4 = RGB(74, 112, 139)

    SLATEBLUE = RGB(106, 90, 205)

    SLATEBLUE1 = RGB(131, 111, 255)

    SLATEBLUE2 = RGB(122, 103, 238)

    SLATEBLUE3 = RGB(105, 89, 205)

    SLATEBLUE4 = RGB(71, 60, 139)

    SLATEGRAY = RGB(112, 128, 144)

    SLATEGRAY1 = RGB(198, 226, 255)

    SLATEGRAY2 = RGB(185, 211, 238)

    SLATEGRAY3 = RGB(159, 182, 205)

    SLATEGRAY4 = RGB(108, 123, 139)

    SNOW1 = RGB(255, 250, 250)

    SNOW2 = RGB(238, 233, 233)

    SNOW3 = RGB(205, 201, 201)

    SNOW4 = RGB(139, 137, 137)

    SPRINGGREEN = RGB(0, 255, 127)

    SPRINGGREEN1 = RGB(0, 238, 118)

    SPRINGGREEN2 = RGB(0, 205, 102)

    SPRINGGREEN3 = RGB(0, 139, 69)

    STEELBLUE = RGB(70, 130, 180)

    STEELBLUE1 = RGB(99, 184, 255)

    STEELBLUE2 = RGB(92, 172, 238)

    STEELBLUE3 = RGB(79, 148, 205)

    STEELBLUE4 = RGB(54, 100, 139)

    TAN = RGB(210, 180, 140)

    TAN1 = RGB(255, 165, 79)

    TAN2 = RGB(238, 154, 73)

    TAN3 = RGB(205, 133, 63)

    TAN4 = RGB(139, 90, 43)

    TEAL = RGB(0, 128, 128)

    THISTLE = RGB(216, 191, 216)

    THISTLE1 = RGB(255, 225, 255)

    THISTLE2 = RGB(238, 210, 238)

    THISTLE3 = RGB(205, 181, 205)

    THISTLE4 = RGB(139, 123, 139)

    TOMATO1 = RGB(255, 99, 71)

    TOMATO2 = RGB(238, 92, 66)

    TOMATO3 = RGB(205, 79, 57)

    TOMATO4 = RGB(139, 54, 38)

    TURQUOISE = RGB(64, 224, 208)

    TURQUOISE1 = RGB(0, 245, 255)

    TURQUOISE2 = RGB(0, 229, 238)

    TURQUOISE3 = RGB(0, 197, 205)

    TURQUOISE4 = RGB(0, 134, 139)

    TURQUOISEBLUE = RGB(0, 199, 140)

    VIOLET = RGB(238, 130, 238)

    VIOLETRED = RGB(208, 32, 144)

    VIOLETRED1 = RGB(255, 62, 150)

    VIOLETRED2 = RGB(238, 58, 140)

    VIOLETRED3 = RGB(205, 50, 120)

    VIOLETRED4 = RGB(139, 34, 82)

    WARMGREY = RGB(128, 128, 105)

    WHEAT = RGB(245, 222, 179)

    WHEAT1 = RGB(255, 231, 186)

    WHEAT2 = RGB(238, 216, 174)

    WHEAT3 = RGB(205, 186, 150)

    WHEAT4 = RGB(139, 126, 102)

    WHITE1 = RGB(255, 255, 255)

    WHITESMOKE = RGB(245, 245, 245)

    YELLOW1 = RGB(255, 255, 0)

    YELLOW2 = RGB(238, 238, 0)

    YELLOW3 = RGB(205, 205, 0)

    YELLOW4 = RGB(139, 139, 0)


COLORS: dict[str, RGB] = {color.name.lower(): color.value for color in ColorConstants}
"""All available colors as a dictionary."""
