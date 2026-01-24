document.addEventListener('DOMContentLoaded', () => {
    const guessSelect = document.getElementById('guess');
    const diceResult = document.getElementById('dice-result');
    const moneyDisplay = document.getElementById('money');
    const diceBtn = document.getElementById('dice-btn');
    const diceForm = document.getElementById('dice-form');
    const diceAmountInput = document.getElementById('dice-amount');
    const diceMessage = document.getElementById('dice-message');
    const csrfToken = diceForm.querySelector('input[name="csrfmiddlewaretoken"]')?.value;
    let isSubmitting = false;

    let isRolling = false;

    diceBtn.addEventListener('click', () => {
        if (isRolling) return; // 連打防止
        isRolling = true;

        diceBtn.textContent = '転がっています…';
        moneyDisplay.textContent = '---';

        let speed = 60;
        let rollCount = 0;

        function rollDice() {
            const dice = Math.floor(Math.random() * 6) + 1;
            diceResult.textContent = `🎲 ${dice}`;
            rollCount++;

            speed += 15;

            if (rollCount < 20) {
                setTimeout(rollDice, speed);
            } else {
                // 完全停止処理
                const guess = Number(guessSelect.value);
                let money;

                if (dice === guess) {
                    money = dice * 200;
                } else {
                    money = 100;
                }

                moneyDisplay.textContent = `${money}円`;
                diceAmountInput.value = money;
                diceBtn.textContent = 'サイコロを振る';
                isRolling = false;
                if (!isSubmitting) {
                    isSubmitting = true;
                    fetch(diceForm.action || window.location.href, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'X-Requested-With': 'XMLHttpRequest',
                            'X-CSRFToken': csrfToken || '',
                        },
                        body: new URLSearchParams({ amount: String(money) }).toString(),
                    })
                        .then((res) => res.json())
                        .then((data) => {
                            if (data && typeof data.saved_amount === 'number') {
                                diceMessage.textContent = `¥${data.saved_amount.toLocaleString()} を貯金しました！`;
                            }
                        })
                        .finally(() => {
                            isSubmitting = false;
                        });
                }
            }
        }

        rollDice();
    });
});
