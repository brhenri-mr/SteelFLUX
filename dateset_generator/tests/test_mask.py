from gerdau.mask import mask_generate



def test_fileNotExist():
    '''
    Testando se um arquivo não existe
    '''
    assert not mask_generate('Test')
