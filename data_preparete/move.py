from glob import glob
import os
import shutil


URL = r'C:\Users\Breno HM Rodrigues\Desktop\Mestrado\Algortimo\gerdau\dateset_generator\data'
DESTINE = r'C:\Users\Breno HM Rodrigues\Desktop\Mestrado\Algortimo\gerdau\data_preparete\data'


subfolder = ['frontal', 'lateral', 'top']
folder = ['base', 'img', 'mask']
index = ['c8041059-7ba4-456f-bf7b-ddb03760b54b',
 'e4adb08c-7ad8-4b05-9e95-9647f26a98e5',
 '1b09f1d3-90cc-4f0c-bda9-228e5062d5f6',
 'a73f1b13-8081-485b-be0c-aa42f7975ddd',
 '1b9f45a6-5129-40db-82b8-1392aa8ad507',
 '3e96d69f-6880-483f-9784-5d7f7f423d21',
 'e0a9f63c-faa9-475f-ae09-21f7be2d3ae4',
 '3afa966f-518f-4da2-86f7-b16c0b088c7e',
 '9b2daab4-5bcd-4e60-92f1-06eb2089b278',
 '50e2fe8a-44fb-4fdb-81dc-c01fb18dbd91',
 '9c8d531b-98fd-45f7-9b3f-9defaa7e8734',
 'f9bd1925-3546-4e4d-a241-a560a9571e97',
 '79145ae5-ab78-4b53-8aad-b3d4a7915c54',
 '14332205-f354-4c40-856c-0a3683a82a1b',
 '8fff08f4-b14c-400e-a86f-c11724e89ab1',
 'b0222c8a-243d-4e15-993a-df5d68a19803',
 '71f1d267-8e38-483e-aba2-1866de31cd1b',
 'b4f597ad-b299-4b56-b142-ec127f843450',
 '9591bc70-896d-4784-a4c5-b4a2fff42475',
 'd437c4cb-4dd6-4565-abda-3645e025e896',
 '3ebfb3fe-d696-4721-aa72-9ec6fe05fd2f',
 '8b8d7b6a-002d-4b2b-bc6e-83cd9fbecdf5']


print(len(index))

for element in folder:
    for el in subfolder:
        destino = os.path.join(DESTINE, element, el)
        for img in glob(os.path.join(URL, element, el, '*.png')):
            if img.split("\\")[-1].replace('.png', '') in index:
                # Ou simplesmente indicar a pasta destino (mantém o nome do arquivo)
                shutil.copy(img, destino)



