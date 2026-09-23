function renderCard(index) {
    const card = CARDS[index];

    // Always reset to question face when moving to a new card
    isFlipped = false;
    cardBody.classList.remove('flipped');

    // Front face
    cardQuestion.textContent = card.question;

    // Back face — correct answer only
    answerLetter.textContent = card.correct_letter;
    answerText.textContent   = card.correct_text;

    // Progress updates
    const pct = ((index + 1) / TOTAL) * 100;
    progressBar.style.width  = pct + '%';
    progressText.textContent = `Card ${index + 1} of ${TOTAL}`;
    cardCounter.textContent  = `${index + 1} / ${TOTAL}`;

    btnPrev.disabled = index === 0;
    btnNext.textContent = index === TOTAL - 1 ? 'Finish ✓' : 'Next →';
}

function flipCard() {
    isFlipped = !isFlipped;
    cardBody.classList.toggle('flipped', isFlipped);
}
