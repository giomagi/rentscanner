a = "g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."
b = "cdefghijklmnopqrstuvwxyzab"
c = ""

for ch in a:
    try:
        c += b[ord(ch) - 97]
    except:
        c += ch

print c
