from PIL import Image
im = Image.open(r"D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\screenshots\\bluemask.png")
im.crop((480,180,1000,420)).resize((1560,720), Image.LANCZOS).save(r"D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\screenshots\\far.png")
im2 = Image.open(r"C:\\Users\\17242\\.dsh\\attachments\\v1\\objects\\08\\088af5ea1b130eaa39769c33950354f9992d4d7710ba0050f4e058785e5d1a46")
im2.crop((480,180,1000,420)).resize((1560,720), Image.LANCZOS).save(r"D:\trae_project\ucf1.7-modifier\06-测试\ucf_mod\screenshots\\far_orig.png")
