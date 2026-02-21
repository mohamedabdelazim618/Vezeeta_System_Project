// ui.js — ripple effect and floating bubbles initializer
(function () {
    function makeRipple(e) {
        var btn = e.currentTarget;
        var rect = btn.getBoundingClientRect();
        var r = document.createElement('span');
        r.className = 'ripple';
        var size = Math.max(rect.width, rect.height) * 1.2;
        r.style.width = r.style.height = size + 'px';
        r.style.left = (e.clientX - rect.left - size / 2) + 'px';
        r.style.top = (e.clientY - rect.top - size / 2) + 'px';
        btn.style.position = btn.style.position || 'relative';
        btn.appendChild(r);
        r.addEventListener('animationend', function () { r.remove(); });
    }

    function attachRipples() {
        document.querySelectorAll('.btn').forEach(function (b) {
            b.addEventListener('click', makeRipple);
        });
    }

    function seedBubbles() {
        document.querySelectorAll('.floating-bubbles').forEach(function (container) {
            if (container.children.length === 0) {
                var s1 = document.createElement('span'); s1.className = 'b1';
                var s2 = document.createElement('span'); s2.className = 'b2';
                container.appendChild(s1); container.appendChild(s2);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', function () {
        attachRipples();
        seedBubbles();
    });

})();
