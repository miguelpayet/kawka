const calcular = idproducto => {
    calcular_precio_p(idproducto).then(idproducto => sumar_total_p(idproducto));
}

const calcular_precio_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        try {
            const _cantidad = document.getElementById("cantidad-" + idproducto).value;
            const _variacion_parent = document.getElementById("variaciones-" + idproducto);
            let _vars = '';
            if (_variacion_parent) {
                const _variaciones = _variacion_parent.querySelectorAll('input[type="checkbox"]:checked');
                const _regex = /variacion-([0-9]+)/;
                _variaciones.forEach((item, idx, array) => {
                    _vars += `${item.id.split(_regex)[1]}${(idx === array.length - 1) ? '' : ','}`;
                });
            }
            fetch(`/sumar/?producto=${idproducto}&cantidad=${_cantidad}` + (_vars.length > 0 ? `&variacion=${_vars}` : ''), {
                method: 'get'
            })
                .then(response => {
                    if (!response.ok) {
                        throw response;
                    }
                    return response.json();
                })
                .then(jsonData => {
                    const _el = document.getElementById('total-' + idproducto);
                    _el.value = jsonData['precio'];
                    resolve(idproducto)
                })
                .catch(err => {
                    reject(err);
                })
        } catch (err) {
            reject(err)
        }
    });
}

const costo_delivery_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        const tipo = document.querySelector('input[name="opciones_entrega"]:checked').value
        if (tipo === 'delivery') {
            fetch('/delivery/', {method: 'get'})
                .then(response => {
                    // console.log(response);
                    if (!response.ok) {
                        throw response;
                    }
                    return response.json();
                })
                .then(jsonData => {
                    // console.log(jsonData);
                    const costo_delivery = parseInt(jsonData['delivery']);
                    // console.log(costo_delivery);
                    const _el = document.getElementById('order-total');
                    _el.value = _el.value + costo_delivery;
                    // console.log(_el.value);
                    resolve(idproducto);
                })
                .catch(err => {
                    console.log(err);
                    reject(err)
                });
        }
    });
}

const delivery_delivery = () => {
    set_input_direccion("visible", true)
}

const delivery_pickup = () => {
    set_input_direccion("hidden", false)
}

const requerir_opcion_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        try {
            const _cantidad = document.getElementById("cantidad-" + idproducto);
            const _opciones = document.getElementById("opciones-" + idproducto);
            if (_opciones) {
                const _radios = Array.from(_opciones.getElementsByTagName("input"));
                if (_cantidad.value > 0) {
                    _radios.forEach(radio => {
                        radio.setAttribute("required", "")
                    });
                } else {
                    _radios.forEach(radio => {
                        radio.removeAttribute("required")
                    });
                }
            }
            resolve(idproducto);
        } catch (err) {
            reject(err);
        }
    });
}

const restar = idproducto => {
    restar_p(idproducto)
        .then(idproducto => calcular_precio_p(idproducto))
        .then(idproducto => requerir_opcion_p(idproducto))
        .then(idproducto => sumar_total_p(idproducto))
        .catch(err => console.log(err));
}

const restar_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        try {
            const _el = document.getElementById("cantidad-" + idproducto);
            if (_el.value > 0) {
                _el.value--;
            }
            resolve(idproducto)
        } catch (err) {
            reject(err);
        }
    });
}

const set_input_direccion = (tipo, requerido) => {
    const _label = document.getElementById("direccion-label");
    _label.style.visibility = tipo;
    const _input = document.getElementById("direccion");
    _input.style.visibility = tipo;
    if (requerido) {
        _input.setAttribute("required", "")
    } else {
        _input.removeAttribute("required")
    }
    sumar_total_p(0).then(idproducto => costo_delivery_p(idproducto));
}

const sumar_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        try {
            const _el = document.getElementById("cantidad-" + idproducto);
            _el.value++;
            resolve(idproducto)
        } catch (err) {
            reject(err);
        }
    });
}

const sumar_total_p = (idproducto) => {
    return new Promise((resolve, reject) => {
        try {
            let gran_total = 0;
            document.forms[0].querySelectorAll('input[id^=total]').forEach(child => {
                gran_total += Number(child.value);
            });
            const _el = document.getElementById('order-total');
            _el.value = gran_total;
            resolve(idproducto);
        } catch (err) {
            reject(err);
        }
    });
}

const sumar = idproducto => {
    sumar_p(idproducto)
        .then(idproducto => calcular_precio_p(idproducto))
        .then(idproducto => requerir_opcion_p(idproducto))
        .then(idproducto => sumar_total_p(idproducto))
        .then(idproducto => costo_delivery_p(idproducto))
        .catch(err => console.log(err));
}

console.log('cargado');