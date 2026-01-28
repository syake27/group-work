document.addEventListener('DOMContentLoaded', () => {
    const amounts = [
        100, 150, 200, 250, 300,
        350, 400, 450, 500, 550,
        600, 650, 700, 750, 800,
        850, 900, 950, 1000
    ];

    let isRunning = false;
    let isStopping = false;
    let speed = 60;
    let timeoutId = null;

    const rouletteBtn = document.getElementById('roulette-btn');
    const amountDisplay = document.getElementById('amount');
    const amountInput = document.getElementById('roulette-amount');
    const rouletteForm = document.getElementById('roulette-form');
    let isSubmitting = false;

    const initialValue = parseInt(amountDisplay.textContent.replace(/\D/g, ''), 10);
    if (!Number.isNaN(initialValue)) {
        amountInput.value = initialValue;
    }

    function spin() {
        if (!isRunning && !isStopping) {
            return;
        }
        const randomIndex = Math.floor(Math.random() * amounts.length);
        amountDisplay.textContent = `${amounts[randomIndex]}円`;
        amountInput.value = amounts[randomIndex];

        if (isRunning || isStopping) {
            timeoutId = setTimeout(spin, speed);
        }
    }

    rouletteBtn.addEventListener('click', () => {

        // ▶ スタート
        if (!isRunning && !isStopping) {
            isRunning = true;
            speed = 60;
            rouletteBtn.textContent = 'ストップ';
            spin();
            return;
        }

        // ⏹ ストップ（減速開始）
        if (isRunning) {
            isRunning = false;
            isStopping = true;
            rouletteBtn.textContent = '🔄';

            const decelerate = setInterval(() => {
                speed += 15;      // ← 増加量を小さく

                if (speed >= 450) { // ← 最終スピードを大きく
                    clearInterval(decelerate);
                    isStopping = false;
                    isRunning = false;
                    if (timeoutId) {
                        clearTimeout(timeoutId);
                        timeoutId = null;
                    }
                    rouletteBtn.textContent = 'スタート';
                    if (!isSubmitting && amountInput.value) {
                        const displayValue = parseInt(amountDisplay.textContent.replace(/\D/g, ''), 10);
                        if (!Number.isNaN(displayValue)) {
                            amountInput.value = displayValue;
                        }
                        isSubmitting = true;
                        rouletteForm.submit();
                    }
                }
            }, 250);               // ← 間隔も少し長く

        }
    });
});
