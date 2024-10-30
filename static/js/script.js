        // JavaScript to handle dynamic membership type in change.html modal
        document.querySelectorAll('.change-btn').forEach(button => {
            button.addEventListener('click', function () {
                const membershipType = this.getAttribute('data-membership-type');
                document.getElementById('membership-type-name').textContent = membershipType;
                document.getElementById('membership-type-input').value = membershipType;
            });
        });