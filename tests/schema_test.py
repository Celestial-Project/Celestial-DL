import testing_utils

def test_schema_keys() -> None:
    
    intents_th = testing_utils.load_json('./data/intents_th.json')['intents_th']
    intents_en = testing_utils.load_json('./data/intents_en.json')['intents_en']
    
    intents = intents_th + intents_en
    
    for intent in intents:
        
        if len(intent.keys()) == 3:
            assert {'tag', 'patterns', 'responses'} == set(intent.keys())
        
        elif len(intent.keys()) == 5:
            assert {'tag', 'date', 'month', 'patterns', 'responses'} == set(intent.keys())
            assert {'fes', 'nonfes'} == set(intent['responses'].keys())
            
        else:
            raise KeyError(f'Invalid key at "{intent["tag"]}". An intents must have "tag", "patterns", "responses" keys.')
        
    unknown_responses = testing_utils.load_json('./data/unknown_responses.json')
    
    assert unknown_responses['en']
    assert unknown_responses['th']
        
        
def test_schema_values() -> None:
    
    intents_th = testing_utils.load_json('./data/intents_th.json')['intents_th']
    intents_en = testing_utils.load_json('./data/intents_en.json')['intents_en']
    
    intents = intents_th + intents_en
    
    for intent in intents:
        
        if len(intent.keys()) == 3:
            assert intent['tag']
            assert intent['patterns']
            assert intent['responses']
        
        elif len(intent.keys()) == 5:
            
            assert intent['tag']
            assert intent['date']
            
            if isinstance(intent['date'], list):
                assert intent['date'][0] in range(1, 32)
                assert intent['date'][1] in range(1, 32)
                assert intent['date'][0] < intent['date'][1]
                
            elif isinstance(intent['date'], int):
                assert intent['date'] in range(1, 32)
                
            assert intent['month']
            assert intent['month'] in range(1, 13)
            assert intent['patterns']
            assert intent['responses']['fes']
            assert intent['responses']['nonfes']