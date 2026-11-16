import { onMounted, ref } from 'vue';

const CAPTCHA_LENGTH = 4;
const CAPTCHA_CHARS = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const CANVAS_WIDTH = 120;
const CANVAS_HEIGHT = 40;

const randomNumber = (min: number, max: number) => Math.floor(Math.random() * (max - min)) + min;
const randomChar = () => CAPTCHA_CHARS[Math.floor(Math.random() * CAPTCHA_CHARS.length)];
const randomColor = (alpha = 1) => `hsla(${randomNumber(0, 360)}, ${randomNumber(50, 80)}%, ${randomNumber(35, 55)}%, ${alpha})`;

export const useCaptcha = () => {
	const canvasRef = ref<HTMLCanvasElement | null>(null);
	const captchaCode = ref('');

	const draw = () => {
		const canvas = canvasRef.value;
		if (!canvas) return;
		const context = canvas.getContext('2d');
		if (!context) return;

		const ratio = window.devicePixelRatio || 1;
		canvas.width = CANVAS_WIDTH * ratio;
		canvas.height = CANVAS_HEIGHT * ratio;
		canvas.style.width = `${CANVAS_WIDTH}px`;
		canvas.style.height = `${CANVAS_HEIGHT}px`;
		context.setTransform(ratio, 0, 0, ratio, 0, 0);
		context.clearRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

		context.fillStyle = '#ffffff';
		context.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

		for (let i = 0; i < 50; i++) {
			context.fillStyle = randomColor(0.45);
			context.beginPath();
			context.arc(randomNumber(0, CANVAS_WIDTH), randomNumber(0, CANVAS_HEIGHT), randomNumber(0.5, 2), 0, Math.PI * 2);
			context.fill();
		}

		for (let i = 0; i < 4; i++) {
			context.strokeStyle = randomColor(0.35);
			context.lineWidth = 1;
			context.beginPath();
			context.moveTo(randomNumber(0, CANVAS_WIDTH), randomNumber(0, CANVAS_HEIGHT));
			context.quadraticCurveTo(randomNumber(0, CANVAS_WIDTH), randomNumber(0, CANVAS_HEIGHT), randomNumber(0, CANVAS_WIDTH), randomNumber(0, CANVAS_HEIGHT));
			context.stroke();
		}

		const step = CANVAS_WIDTH / CAPTCHA_LENGTH;
		for (let i = 0; i < captchaCode.value.length; i++) {
			context.save();
			context.font = `bold ${randomNumber(22, 28)}px Arial`;
			context.fillStyle = randomColor();
			context.textAlign = 'center';
			context.textBaseline = 'middle';
			context.translate(step * (i + 0.5), CANVAS_HEIGHT / 2 + randomNumber(-3, 4));
			context.rotate((randomNumber(-18, 18) * Math.PI) / 180);
			context.fillText(captchaCode.value[i], 0, 0);
			context.restore();
		}
	};

	const refresh = () => {
		captchaCode.value = Array.from({ length: CAPTCHA_LENGTH }, randomChar).join('');
		draw();
	};

	onMounted(refresh);

	return {
		canvasRef,
		captchaCode,
		refresh,
	};
};
