function cond_offset(flow_t) {
  if (flow_t <= 37) return 3.0;
  else if (flow_t <= 52) return 4.0;
  else return 5.0;
}

function evap_offset(out_t) {
  if (out_t >= 5) return 5.0;
  else if (out_t >= 0) return 6.0;
  else if (out_t >= -5) return 7.0;
  else return 8.0;
}

function eta_carnot(out_t, flow_t) {
  let base;
  if (out_t >= 5) base = 0.48;
  else if (out_t >= 0) base = 0.47;
  else if (out_t >= -5) base = 0.45;
  else base = 0.44;
  if (flow_t >= 50) base -= 0.03;
  else if (flow_t >= 40) base -= 0.02;
  return Math.round(base * 1000) / 1000;
}

function arotherm_cop(outdoor_c, flow_c, return_c) {
  const t_cond_sat_k = (flow_c + return_c) / 2 + cond_offset(flow_c) + 273.15;
  const t_evap_sat_k = outdoor_c - evap_offset(outdoor_c) + 273.15;
  const cop_carnot = t_cond_sat_k / (t_cond_sat_k - t_evap_sat_k);
  const eta = eta_carnot(outdoor_c, flow_c);
  const cop_real = eta * cop_carnot;
  return {
    "Outdoor °C": outdoor_c,
    "Flow °C": flow_c,
    "Return °C": return_c,
    "ΔT_cond K": cond_offset(flow_c),
    "ΔT_evap K": evap_offset(outdoor_c),
    "ηCarnot": eta,
    "Carnot COP": Math.round(cop_carnot * 100) / 100,
    "Expected COP": Math.round(cop_real * 100) / 100,
  };
}

document.getElementById('cop-form').addEventListener('submit', function(e) {
  e.preventDefault();
  const outdoor = parseFloat(document.getElementById('outdoor').value);
  const flow = parseFloat(document.getElementById('flow').value);
  const ret = parseFloat(document.getElementById('return').value);
  const result = arotherm_cop(outdoor, flow, ret);

  let html = '<table>';
  for (const [key, val] of Object.entries(result)) {
    html += `<tr><th>${key}</th><td>${val}</td></tr>`;
  }
  html += '</table>';
  const resultDiv = document.getElementById('result');
  resultDiv.innerHTML = html;
  resultDiv.style.display = '';
});
