
void FUN_0000368c(int param_1)

{
  undefined1 *puVar1;
  int *piVar2;
  uint extraout_r1;
  uint extraout_r1_00;
  undefined4 extraout_r2;
  undefined4 extraout_r2_00;
  undefined4 extraout_r2_01;
  undefined4 extraout_r2_02;
  undefined4 extraout_r2_03;
  undefined4 extraout_r2_04;
  undefined4 extraout_r2_05;
  undefined4 uVar3;
  undefined4 extraout_r2_06;
  undefined4 extraout_r3;
  undefined4 extraout_r3_00;
  undefined4 extraout_r3_01;
  undefined4 extraout_r3_02;
  undefined4 extraout_r3_03;
  undefined4 extraout_r3_04;
  undefined4 extraout_r3_05;
  undefined4 uVar4;
  undefined4 extraout_r3_06;
  uint uVar5;
  uint uVar6;
  undefined4 uVar7;
  
  uVar7 = 0;
  FUN_0003451c(0x18,0x88,&DAT_000037a8,0x18,0);
  FUN_0003ca68(0xd000,DAT_000037b8,0x1000);
  piVar2 = DAT_000037bc;
  FUN_000003c0(&DAT_000037c0,(uint)*(byte *)(*DAT_000037bc + 0x3c),extraout_r2,extraout_r3);
  puVar1 = DAT_000037b8;
  uVar5 = 0;
  uVar6 = extraout_r1;
  uVar3 = extraout_r2_00;
  uVar4 = extraout_r3_00;
  while (((uVar5 < (uint)*(byte *)(*piVar2 + 0x3c) * 0x24 && (puVar1[(uVar5 / 0x24) * 0x24] != -1))
         && (puVar1[(uVar5 / 0x24) * 0x24 + 1] != -1))) {
    if ((uVar5 == (uVar5 / 0x24) * 0x24) &&
       (FUN_000003c0(s_%d:_000037cc,uVar5 / 0x24,uVar3,uVar4), uVar3 = extraout_r2_01,
       uVar4 = extraout_r3_01, param_1 == 1)) {
      FUN_0003ca68((uVar5 / 0x24) * 0x1000 + 0x300000,DAT_000037d4,0x1000);
      uVar3 = extraout_r2_02;
      uVar4 = extraout_r3_02;
      for (uVar6 = 0;
          uVar6 < ((uint)(byte)puVar1[(uVar5 / 0x24) * 0x24 + 0x10] +
                  (uint)(byte)puVar1[(uVar5 / 0x24) * 0x24 + 0xf] * 0x100) * 10;
          uVar6 = uVar6 + 1 & 0xffff) {
        if (uVar6 == (uVar6 / 10) * 10) {
          FUN_000003c0(s_---%d:_000037d8,uVar6 / 10,uVar3,uVar4);
          uVar3 = extraout_r2_03;
          uVar4 = extraout_r3_03;
        }
        FUN_000003c0(&DAT_000037e4,(uint)(byte)DAT_000037d4[uVar6],uVar3,uVar4);
        uVar3 = extraout_r2_04;
        uVar4 = extraout_r3_04;
      }
      FUN_000003c0(s_--%d:_000037ec,uVar5 / 0x24,uVar3,uVar4);
      uVar3 = extraout_r2_05;
      uVar4 = extraout_r3_05;
    }
    FUN_000003c0(&DAT_000037e4,(uint)(byte)puVar1[uVar5],uVar3,uVar4);
    uVar5 = uVar5 + 1 & 0xffff;
    uVar6 = extraout_r1_00;
    uVar3 = extraout_r2_06;
    uVar4 = extraout_r3_06;
  }
  FUN_000003c0(&DAT_000037f8,uVar6,uVar3,uVar7);
  return;
}

