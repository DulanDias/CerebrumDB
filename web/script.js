document.addEventListener("DOMContentLoaded", () => {
    console.log("Welcome to CerebrumDB!");
    const ctaButtons = document.querySelectorAll(".cta-button");

    ctaButtons.forEach(button => {
        button.addEventListener("click", () => {
            console.log(`Navigating to ${button.getAttribute("href")}`);
        });
    });

    const faqQuestions = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(button => {
        button.addEventListener('click', () => {
            const answer = button.nextElementSibling;
            const isVisible = answer.style.display === 'block';

            // Collapse all other answers
            document.querySelectorAll('.faq-answer').forEach(ans => {
                ans.style.display = 'none';
            });

            // Toggle the clicked answer
            answer.style.display = isVisible ? 'none' : 'block';
        });
    });
});
