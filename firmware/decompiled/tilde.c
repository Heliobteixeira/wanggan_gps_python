
void FUN_000060e0(void)

{
  int iVar1;
  undefined1 *puVar2;
  uint uVar3;
  uint extraout_r1;
  uint extraout_r1_00;
  uint extraout_r1_01;
  uint extraout_r1_02;
  uint extraout_r1_03;
  uint extraout_r1_04;
  undefined4 extraout_r2;
  undefined4 extraout_r2_00;
  undefined4 extraout_r2_01;
  undefined4 extraout_r2_02;
  undefined4 extraout_r2_03;
  undefined4 extraout_r2_04;
  undefined4 extraout_r2_05;
  undefined4 extraout_r2_06;
  undefined4 extraout_r2_07;
  undefined4 extraout_r2_08;
  undefined4 extraout_r2_09;
  undefined4 extraout_r2_10;
  undefined4 extraout_r2_11;
  undefined4 uVar4;
  undefined4 extraout_r3;
  undefined4 extraout_r3_00;
  undefined4 extraout_r3_01;
  undefined4 extraout_r3_02;
  undefined4 extraout_r3_03;
  uint uVar5;
  undefined4 extraout_r3_04;
  undefined4 extraout_r3_05;
  undefined4 extraout_r3_06;
  undefined4 extraout_r3_07;
  undefined4 extraout_r3_08;
  undefined4 extraout_r3_09;
  undefined4 extraout_r3_10;
  undefined4 extraout_r3_11;
  undefined4 uVar6;
  uint uVar7;
  byte *pbVar8;
  uint uVar9;
  uint uVar10;
  uint uVar11;
  uint uVar12;
  uint uVar13;
  ushort local_6c;
  byte local_6a;
  byte local_69;
  ushort local_60;
  undefined4 local_5c;
  undefined4 uStack_58;
  ushort local_42;
  char local_3e;
  uint local_3c;
  uint local_38;
  uint local_34;
  uint local_30;
  uint local_2c;
  uint local_28;
  
  iVar1 = DAT_000064b0;
  local_38 = (uint)(ushort)(*(short *)(DAT_000064b0 + 0x38) + *(short *)(DAT_000064b0 + 0x3a));
  FUN_000072b0();
  if (1000 < local_38) {
    local_38 = 0;
  }
  uVar12 = local_38 +
           (uint)*(ushort *)(iVar1 + 0x2a) + (uint)*(byte *)(iVar1 + 0x34) +
           (uint)*(byte *)(iVar1 + 0x36);
  uVar10 = 0;
  do {
    uVar7 = DAT_00006544;
    if (local_38 <= uVar10) {
      local_28 = *(ushort *)(DAT_000064b0 + 0x2a) + 100;
      for (uVar10 = 100; uVar10 < local_28; uVar10 = uVar10 + 1) {
        if (uVar10 == 100) {
          FUN_0003ca68(DAT_00006548,DAT_00006504,0x1000);
        }
        if ((uVar10 & 0xff) == 0) {
          FUN_0003ca68(DAT_00006548 + (uVar10 >> 8) * 0x1000,DAT_00006504,0x1000);
        }
        uVar13 = uVar10 & 0xff;
        if ((uVar10 & 0xff) == 0) {
          uVar13 = uVar13 + 0x100;
        }
        uVar13 = FUN_0003fb84(uVar13 - 99 & 0xffff);
        *(char *)(DAT_0000654c + 1) = (char)uVar13;
        if (uVar13 >> 4 == 1) {
          local_3c = 0x2b;
        }
        else {
          local_3c = 0x2d;
        }
        pbVar8 = DAT_00006504 + (uVar10 & 0xff) * 0x10;
        if (*pbVar8 < 0x30) {
          FUN_000003c0(s_n%04d,p%010d,p%010d;t%04d%02d%02_00006550,1,0,0);
        }
        else {
          FUN_000003c0(s_n%04d,p%010d,p%010d;t%04d%02d%02_00006550,1,0,0);
        }
        FUN_0003e338(5);
        uVar13 = (uint)pbVar8[7] * 0x10000 + (uint)pbVar8[8] * 0x100 + (uint)pbVar8[9];
        if ((uint)pbVar8[0xf] + (uint)pbVar8[0xe] * 0x100 < 60000) {
          FUN_000003c0(&DAT_0000697c,local_3c,(uint)pbVar8[6],uVar13 / uVar7);
        }
        else {
          FUN_000003c0(&DAT_0000697c,local_3c,(uint)pbVar8[6],uVar13 / uVar7);
        }
        FUN_0003e338(3);
      }
      FUN_0003ca68(DAT_000069b8,DAT_000069b4,0x2000);
      local_38 = (uint)*(byte *)(DAT_000069bc + 0x34);
      for (uVar10 = 0; puVar2 = DAT_000069b4, uVar10 < local_38; uVar10 = uVar10 + 1) {
        uVar5 = (uint)CONCAT11(DAT_000069b4[uVar10 * 0x20 + 0xe],DAT_000069b4[uVar10 * 0x20 + 0xf]);
        FUN_0003ca68(DAT_000069c0 + uVar10 * 0x1000,DAT_000069c4,0x1000);
        FUN_000003c0(s_n%04d,e%010d,m%010d;t%04d%02d%02_000069c8,uVar5,
                     (uint)(byte)puVar2[uVar10 * 0x20 + 0xd] +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 10] * 0x1000000 +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 0xb] * 0x10000 +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 0xc] * 0x100,
                     (uint)(byte)puVar2[uVar10 * 0x20 + 9] +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 6] * 0x1000000 +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 7] * 0x10000 +
                     (uint)(byte)puVar2[uVar10 * 0x20 + 8] * 0x100);
        FUN_0003e338(5);
        for (uVar13 = 0; uVar13 < uVar5; uVar13 = uVar13 + 1) {
          uVar9 = (uint)(byte)DAT_000069c4[uVar13 * 10 + 1] * 0x10000 +
                  (uint)(byte)DAT_000069c4[uVar13 * 10 + 2] * 0x100 +
                  (uint)(byte)DAT_000069c4[uVar13 * 10 + 3];
          local_2c = (uint)(byte)DAT_000069c4[uVar13 * 10 + 9] +
                     (uint)(byte)DAT_000069c4[uVar13 * 10 + 8] * 0x100;
          if (local_2c < 60000) {
            FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                         (uint)(byte)DAT_000069c4[uVar13 * 10],uVar9 / uVar7,
                         ((uVar9 - uVar7 * (uVar9 / uVar7)) * 0x3c) / uVar7);
            uVar9 = extraout_r1_00;
            uVar4 = extraout_r2_01;
            uVar6 = extraout_r3_01;
          }
          else {
            FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                         (uint)(byte)DAT_000069c4[uVar13 * 10],uVar9 / uVar7,
                         ((uVar9 - uVar7 * (uVar9 / uVar7)) * 0x3c) / uVar7);
            uVar9 = extraout_r1_01;
            uVar4 = extraout_r2_02;
            uVar6 = extraout_r3_02;
          }
          if (uVar13 == uVar5 - 1) {
            FUN_000003c0(&DAT_0000653c,uVar9,uVar4,uVar6);
          }
          else {
            FUN_000003c0(&DAT_000069b0,uVar9,uVar4,uVar6);
          }
          FUN_0003e338(3);
        }
      }
      FUN_0003ca68(DAT_000069fc,DAT_000069b4,0x1000);
      local_38 = (uint)*(byte *)(DAT_000069bc + 0x36);
      uVar10 = extraout_r1_02;
      uVar4 = extraout_r2_03;
      uVar6 = extraout_r3_03;
      for (uVar13 = 0; uVar13 < local_38; uVar13 = uVar13 + 1) {
        uVar9 = (uint)(ushort)((ushort)(byte)DAT_000069b4[uVar13 * 0x24 + 0xf] * 0x100 +
                              (ushort)(byte)DAT_000069b4[uVar13 * 0x24 + 0x10]);
        uVar5 = (uint)(ushort)((ushort)(byte)DAT_000069b4[uVar13 * 0x24 + 0x22] * 0x100 +
                              (ushort)(byte)DAT_000069b4[uVar13 * 0x24 + 0x23]);
        FUN_000003c0(s_n%04d,k%010d,l%010d;t%04d%02d%02_00006a00,uVar9,
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 9] +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 6] * 0x1000000 +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 7] * 0x10000 +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 8] * 0x100,
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 0xd] +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 10] * 0x1000000 +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 0xb] * 0x10000 +
                     (uint)(byte)DAT_000069b4[uVar13 * 0x24 + 0xc] * 0x100);
        FUN_0003e338(5);
        uVar10 = extraout_r1_03;
        uVar4 = extraout_r2_04;
        uVar6 = extraout_r3_04;
        for (uVar11 = 0; uVar11 < uVar9 / 0x199; uVar11 = uVar11 + 1) {
          FUN_0003ca68(DAT_00006a34 + (uVar5 + uVar11) * 0x1000,DAT_000069c4,0x1000);
          uVar10 = 0;
          do {
            uVar3 = (uint)(byte)DAT_000069c4[uVar10 * 10 + 1] * 0x10000 +
                    (uint)(byte)DAT_000069c4[uVar10 * 10 + 2] * 0x100 +
                    (uint)(byte)DAT_000069c4[uVar10 * 10 + 3];
            local_30 = (uint)(byte)DAT_000069c4[uVar10 * 10 + 9] +
                       (uint)(byte)DAT_000069c4[uVar10 * 10 + 8] * 0x100;
            if (local_30 < 60000) {
              FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                           (uint)(byte)DAT_00006d38[uVar10 * 10],uVar3 / uVar7,
                           ((uVar3 - uVar7 * (uVar3 / uVar7)) * 0x3c) / uVar7);
              uVar4 = extraout_r2_05;
              uVar6 = extraout_r3_05;
            }
            else {
              FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                           (uint)(byte)DAT_000069c4[uVar10 * 10],uVar3 / uVar7,
                           ((uVar3 - uVar7 * (uVar3 / uVar7)) * 0x3c) / uVar7);
              uVar4 = extraout_r2_06;
              uVar6 = extraout_r3_06;
            }
            if (((uVar9 % 0x199 == 0) && (uVar9 / 0x199 - 1 == uVar11)) && (uVar10 == 0x198)) {
              FUN_000003c0(&DAT_0000653c,0,uVar4,uVar6);
            }
            else {
              FUN_000003c0(&DAT_000069b0,uVar9 % 0x199,uVar4,uVar6);
            }
            FUN_0003e338(3);
            uVar10 = uVar10 + 1;
          } while (uVar10 < 0x199);
          uVar10 = extraout_r1_04;
          uVar4 = extraout_r2_07;
          uVar6 = extraout_r3_07;
        }
        if (uVar9 % 0x199 != 0) {
          FUN_0003ca68(DAT_00006d3c + (uVar5 + uVar11) * 0x1000,DAT_00006d38,0x1000);
          uVar4 = extraout_r2_08;
          uVar6 = extraout_r3_08;
          for (uVar5 = 0; uVar10 = uVar9 / 0x199, uVar5 < uVar9 % 0x199; uVar5 = uVar5 + 1) {
            uVar10 = (uint)(byte)DAT_00006d38[uVar5 * 10 + 1] * 0x10000 +
                     (uint)(byte)DAT_00006d38[uVar5 * 10 + 2] * 0x100 +
                     (uint)(byte)DAT_00006d38[uVar5 * 10 + 3];
            local_34 = (uint)(byte)DAT_00006d38[uVar5 * 10 + 9] +
                       (uint)(byte)DAT_00006d38[uVar5 * 10 + 8] * 0x100;
            if (local_34 < 60000) {
              FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                           (uint)(byte)DAT_00006d38[uVar5 * 10],uVar10 / uVar7,
                           ((uVar10 - uVar7 * (uVar10 / uVar7)) * 0x3c) / uVar7);
              uVar4 = extraout_r2_09;
              uVar6 = extraout_r3_09;
            }
            else {
              FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,
                           (uint)(byte)DAT_00006d38[uVar5 * 10],uVar10 / uVar7,
                           ((uVar10 - uVar7 * (uVar10 / uVar7)) * 0x3c) / uVar7);
              uVar4 = extraout_r2_10;
              uVar6 = extraout_r3_10;
            }
            if (uVar9 % 0x199 - 1 == uVar5) {
              FUN_000003c0(&DAT_0000653c,uVar9 / 0x199,uVar4,uVar6);
            }
            else {
              FUN_000003c0(&DAT_000069b0,uVar9 / 0x199,uVar4,uVar6);
            }
            FUN_0003e338(3);
            uVar4 = extraout_r2_11;
            uVar6 = extraout_r3_11;
          }
        }
      }
      if (uVar12 == 0) {
        FUN_000003c0(s_null!_00006d40,uVar10,uVar4,uVar6);
      }
      return;
    }
    if (uVar10 < *(ushort *)(DAT_000064b0 + 0x38)) {
      FUN_00007258((undefined1 *)&local_6c,uVar10 & 0xffff);
    }
    else {
      FUN_00007258((undefined1 *)&local_6c,
                   uVar10 - *(ushort *)(DAT_000064b0 + 0x38) & 0xffff | 0x8000);
    }
    if (local_3e == '\0') {
      FUN_000003c0(s_n%04d,m%010d,l%010d;_000064ec,(uint)local_60,local_5c,uStack_58);
    }
    else {
      FUN_000003c0(s_n%04d,l%010d,m%010d;_000064b4,(uint)local_60,uStack_58,local_5c);
    }
    FUN_0003e338(2);
    FUN_000003c0(s_t%d%02d%02d%02d%02d,_000064cc,(uint)local_6c,(uint)local_6a,(uint)local_69);
    FUN_0003e338(2);
    FUN_000003c0(s_N%04d_000064e4,uVar12,extraout_r2,extraout_r3);
    FUN_0003e338(1);
    uVar7 = 0;
LAB_00006320:
    if (local_60 != uVar7) {
      if (uVar7 == (uVar7 / 0x199) * 0x199) {
        FUN_00007298(uVar7 / 0x199 + (uint)local_42 & 0xffff,DAT_00006504);
      }
      uVar13 = 0;
      do {
        uVar5 = (uint)(byte)DAT_00006504[uVar13 * 10 + 3] +
                (uint)(byte)DAT_00006504[uVar13 * 10] * 0x1000000 +
                (uint)(byte)DAT_00006504[uVar13 * 10 + 1] * 0x10000 +
                (uint)(byte)DAT_00006504[uVar13 * 10 + 2] * 0x100;
        if (CONCAT11(DAT_00006504[uVar13 * 10 + 8],DAT_00006504[uVar13 * 10 + 9]) < 60000) {
          FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,uVar5 / DAT_00006508,
                       (uVar5 - DAT_00006508 * (uVar5 / DAT_00006508)) / 60000,
                       (uVar5 % 60000) / 1000);
        }
        else {
          FUN_000003c0(s_%03dd%02d'%02d.%02d",%02dd%02d'%_0000650c,uVar5 / DAT_00006508,
                       (uVar5 - DAT_00006508 * (uVar5 / DAT_00006508)) / 60000,
                       (uVar5 % 60000) / 1000);
        }
        FUN_0003e338(3);
        uVar7 = uVar7 + 1 & 0xffff;
        if (local_60 == uVar7) {
          FUN_000003c0(&DAT_0000653c,extraout_r1,extraout_r2_00,extraout_r3_00);
          break;
        }
        FUN_000003c0(&DAT_00006540,extraout_r1,extraout_r2_00,extraout_r3_00);
        FUN_0003e338(1);
        uVar13 = uVar13 + 1;
      } while (uVar13 < 0x199);
      goto LAB_00006320;
    }
    uVar10 = uVar10 + 1;
  } while( true );
}

