
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

byte FUN_0000fa58(void)

{
  byte bVar1;
  byte *pbVar2;
  ushort *puVar3;
  byte *pbVar4;
  undefined4 extraout_r1;
  undefined4 extraout_r2;
  undefined4 extraout_r3;
  
  FUN_00029090();
  pbVar2 = DAT_0000fc6c;
  switch((uint)*DAT_0000fc6c) {
  case 0:
    FUN_00018a78(0);
    break;
  case 2:
    FUN_00028de0();
    break;
  case 3:
    FUN_0001a37c();
    break;
  case 4:
    FUN_0002aff4();
    break;
  case 5:
    FUN_00008674();
    break;
  case 6:
    FUN_00029e84();
    break;
  case 7:
    FUN_00028438();
    break;
  case 8:
    FUN_00028a0c();
    break;
  case 9:
    FUN_00007e6c((uint)*DAT_0000fc6c);
    break;
  case 10:
    FUN_00025f0c();
    break;
  case 0xc:
    FUN_0001e89c();
    break;
  case 0xd:
    FUN_00026040();
    break;
  case 0xe:
    FUN_00025e24();
    break;
  case 0x12:
    FUN_0000f870();
    break;
  case 0x13:
    FUN_0002ec10();
    break;
  case 0x14:
    FUN_0003197c();
    break;
  case 0x15:
    FUN_0000a8bc();
    break;
  case 0x16:
    FUN_0000ff14();
    break;
  case 0x17:
    FUN_000128dc();
    break;
  case 0x18:
    FUN_000119ac();
    break;
  case 0x1a:
    FUN_0002a828();
    break;
  case 0x1c:
    FUN_000296b0();
    break;
  case 0x1d:
    FUN_000076b8();
    break;
  case 0x1f:
    FUN_00009c40();
    break;
  case 0x20:
    FUN_0002aa9c();
    break;
  case 0x21:
    FUN_000090bc();
    break;
  case 0x22:
    FUN_00008460();
    break;
  case 0x23:
    FUN_00009e94();
    break;
  case 0x24:
    FUN_0000a25c();
    break;
  case 0x25:
    FUN_0001eafc();
    break;
  case 0x26:
    FUN_0000a584();
    break;
  case 0x27:
    FUN_0001f0d4();
    break;
  case 0x2b:
    FUN_0000fc94();
    break;
  case 0x2e:
    FUN_0001c9c8(0,extraout_r1,extraout_r2,extraout_r3);
    break;
  case 0x2f:
    FUN_0001c9c8(1,extraout_r1,extraout_r2,extraout_r3);
    break;
  case 0x31:
    FUN_00026b08(0);
    break;
  case 0x32:
    FUN_00015d3c();
    break;
  case 0x34:
    FUN_00027fc4();
    break;
  case 0x35:
    FUN_000136c0();
    break;
  case 0x36:
    FUN_00011474();
    break;
  case 0x37:
    FUN_0000b664();
    break;
  case 0x39:
    FUN_00008d88();
    break;
  case 0x3a:
    FUN_0000ab1c();
    break;
  case 0x3b:
    FUN_000116cc();
    break;
  case 0x3d:
    FUN_00015f80();
    break;
  case 0x3e:
    FUN_00017964();
    break;
  case 0x3f:
    FUN_00016ec4();
    break;
  case 0x4a:
    *DAT_0000fc6c = 0;
  }
  puVar3 = DAT_0000fc70;
  if ((int)((uint)*DAT_0000fc70 << 0x10) < 0) {
    if (*pbVar2 != 3) {
      bVar1 = *_DAT_0000fc74;
      if (bVar1 == 0x7e) {
        FUN_000060e0();
      }
      else if (bVar1 == 0x21) {
        FUN_0000368c(0);
      }
      else if (bVar1 == 0x5e) {
        FUN_0000368c(1);
      }
      else {
        pbVar4 = FUN_00000780(_DAT_0000fc74,(byte *)(s_Mode_0000fc77 + 1));
        if (pbVar4 != (byte *)0x0) {
          FUN_00003800();
          FUN_0003e338(0x5dc);
          FUN_000098cc(0);
          *DAT_0000fc80 = 0xffff;
          *DAT_0000fc84 = 0;
          FUN_00018a78(1);
          *pbVar2 = 0;
        }
      }
    }
    *puVar3 = 0;
  }
  if (((DAT_0000fc8c < *DAT_0000fc88) && (*pbVar2 != 3)) &&
     (*(char *)(*DAT_0000fc90 + 0x27) != '\x01')) {
    FUN_00039304();
  }
  return *pbVar2;
}

