import request from '/@/utils/request';

export function useSettingsApi() {
	return {
		getTheme: () => request<{ code: number; message: string; data: Record<string, any> }>({ url: '/settings/theme', method: 'get' }),
		saveTheme: (settings: Record<string, any>) =>
			request({ url: '/settings/theme', method: 'put', data: { settings } }),
	};
}
