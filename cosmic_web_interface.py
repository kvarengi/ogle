#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Веб-интерфейс для Робота-Демиурга Сверхновой Мультивселенной
Элегантный французский дизайн для продажи космических тел
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for
from cosmic_demiurge import CosmicDemiurge, CelestialType
import json
import math

app = Flask(__name__)
demiurge = CosmicDemiurge()


@app.route('/')
def index():
    """Главная страница с каталогом"""
    greeting = demiurge.get_poetic_greeting()
    nutation_status = demiurge.get_nutation_status()
    available_bodies = demiurge.browse_catalog()
    
    return render_template('index.html', 
                         greeting=greeting,
                         nutation_status=nutation_status,
                         bodies=available_bodies,
                         universe_rate=demiurge.universe_coins_rate)


@app.route('/api/catalog')
def api_catalog():
    """API для получения каталога"""
    celestial_type = request.args.get('type')
    max_price = request.args.get('max_price', type=float)
    
    if celestial_type:
        try:
            celestial_type = CelestialType(celestial_type)
        except ValueError:
            celestial_type = None
    
    bodies = demiurge.browse_catalog(celestial_type, max_price)
    
    return jsonify([{
        'id': body.id,
        'name': body.name,
        'type': body.type.value,
        'coordinates': body.coordinates,
        'price': body.price_universe_coins,
        'discovery_chance': body.discovery_chance_today,
        'description': body.poetic_description,
        'available': body.is_available,
        'gravitational_params': {
            'mass': body.gravitational_params.mass_kg,
            'radius': body.gravitational_params.radius_m,
            'surface_gravity': body.gravitational_params.surface_gravity,
            'escape_velocity': body.gravitational_params.escape_velocity
        }
    } for body in bodies])


@app.route('/api/reserve', methods=['POST'])
def api_reserve():
    """API для резервирования тела"""
    data = request.json
    body_id = data.get('body_id')
    customer_name = data.get('customer_name')
    hours = data.get('hours', 24)
    
    success = demiurge.reserve_celestial_body(body_id, customer_name, hours)
    
    return jsonify({'success': success})


@app.route('/api/purchase', methods=['POST'])  
def api_purchase():
    """API для покупки тела"""
    data = request.json
    body_id = data.get('body_id')
    customer_name = data.get('customer_name')
    
    success = demiurge.purchase_celestial_body(body_id, customer_name)
    
    if success:
        certificate = demiurge.generate_ownership_certificate(body_id)
        return jsonify({'success': True, 'certificate': certificate})
    else:
        return jsonify({'success': False})


@app.route('/api/nutation')
def api_nutation():
    """API для получения статуса нутации"""
    longitude, obliquity = demiurge.calculate_nutation_influence()
    
    return jsonify({
        'longitude': longitude,
        'obliquity': obliquity,
        'phase': (math.pi * 2 * (demiurge.sacrum_position.period_days)) % 360,
        'status': demiurge.get_nutation_status()
    })


@app.route('/api/discoveries')
def api_discoveries():
    """API для проверки открытий"""
    alerts = demiurge.check_discovery_alerts()
    return jsonify({'alerts': alerts})


@app.route('/certificate/<body_id>')
def certificate(body_id):
    """Страница сертификата владения"""
    if body_id not in demiurge.catalog:
        return "Космическое тело не найдено", 404
    
    body = demiurge.catalog[body_id]
    if not body.owner:
        return "У этого тела нет владельца", 404
    
    certificate_text = demiurge.generate_ownership_certificate(body_id)
    return render_template('certificate.html', 
                         certificate=certificate_text,
                         body=body)


if __name__ == '__main__':
    print("🌌 Запуск веб-интерфейса Демиурга...")
    app.run(debug=True, host='0.0.0.0', port=5000)
