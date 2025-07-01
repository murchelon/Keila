import json
from state.state_manager import state_type
import main


def test_get_info(client):
    main.global_STATE.set_state(state_type.READY)
    resp = client.get('/api/getInfo')
    assert resp.status_code == 200
    data = resp.json()
    assert data['statusCode'] == 'OK'


def test_reload_config(client):
    main.global_STATE.set_state(state_type.READY)
    config_path = 'src/keila_config.json'
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    cfg['language'] = 'en-US'
    with open(config_path, 'w') as f:
        json.dump(cfg, f)

    resp = client.post('/api/reloadConfig')
    assert resp.status_code == 200
    from bib.config import KeilaConfig
    assert KeilaConfig.instance().get('language') == 'en-US'


def test_action_voiceprompt_route(client, monkeypatch):
    main.global_STATE.set_state(state_type.READY)
    monkeypatch.setattr('main.thread_manager_main.start_thread', lambda *a, **k: None)
    resp = client.post('/api/actions/VoicePrompt')
    assert resp.status_code == 200
    assert resp.json()['statusCode'] == 'OK'


def test_cancel_actions(client, monkeypatch):
    main.global_STATE.set_state(state_type.READY)
    monkeypatch.setattr('main.thread_manager_main.stop_all', lambda *a, **k: None)
    resp = client.post('/api/cancelActions')
    assert resp.status_code == 200
    assert resp.json()['statusCode'] == 'OK'
    assert resp.json()['global_STATE'] == state_type.READY.name
