function toggleCard(id) {
    const body = document.getElementById(id);
    const chev = document.getElementById('chev-' + id);
    const open = body.classList.toggle('open');
    chev.classList.toggle('open', open);
}

/* CSS */
.q-body         { display: none; }   /* collapsed by default */
.q-body.open    { display: block; }  /* shown when toggled */
.chevron        { transition: transform 0.2s; }
.chevron.open   { transform: rotate(180deg); }
