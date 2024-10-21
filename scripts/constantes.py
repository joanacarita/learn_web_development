def const_koos_12_crf():

    dict_questionario_options = {"name": ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre'], "value": [0, 1, 2, 3, 4]}

    dict_perg_resp = {
        "pergunta_struct1" : {
            "num_pergunta" : 1,
            "pergunta" : "Tem tido o joelho inchado?",
            "opcoes" : dict_questionario_options
        },
        "pergunta_struct2" : {
            "num_pergunta" : 2,
            "pergunta" : "Tem sentido ranger, ouvido um estalo ou qualquer outro som quando mexe o joelho?",
            "opcoes" : dict_questionario_options
        },
        "pergunta_struct3" : {
            "num_pergunta" : 3,
            "pergunta" : "Tem sentido o joelho preso ou bloqueado quando se mexe?",
            "opcoes" : dict_questionario_options
        }
    }

    return dict_perg_resp