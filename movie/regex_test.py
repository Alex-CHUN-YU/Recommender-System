#-*- encoding: UTF-8 -*-
import re
content = "★勇奪坎城、柏林、威?尼斯;三~大:影展，全部囊括得獎入袋的國寶級大導演★波蘭導演 傑西‧史考利莫？斯基，今年再奪威尼斯兩大獎評審團大獎及最佳男主角獎逃亡 是為了求生，殺戮是為了存活穆罕默德（文森加洛飾）在阿富汗被美軍逮捕，飽受酷刑凌，一日在押送至歐洲某秘密總部盤問途中，囚車不慎墜崖，紛飛大雪中戰俘趁亂逃竄，在這遠離家園的蠻荒之地，他意識到不顧一切逃生是生存唯一手段。眼看自由在望卻身陷冰雪叢林迷宮的他，一方面要躲避美軍攻擊、一方面為了裹腹，他必須殺害大自然動物果腹以求生存…。生性悲憫的他，不願殺害有靈性的動物，但面對窮追不捨的美軍，他卻是格殺勿論。【關於電影】拍攝期間文森加洛為了入戲曾一度禁食、禁言、自殘自己，挑戰體能"
print(content, "\n\n")
content = re.sub(r'\、|\，|★|\。|\?|\？|\;|\；|\:|\~|\：|\⋯', '\n', content)
print(content)
content = re.sub(r"[\s+\.\★\【\】\‧\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+", "", " 傑西‧史考利莫？斯基【關於電影】拍")
print(content)