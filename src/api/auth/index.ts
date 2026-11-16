import request from '/@/utils/request';

export interface LoginResult {
	token: string;
	userName: string;
	roles: string[];
	authBtnList: string[];
	menuPaths: string[];
	userInfos: Record<string, any>;
}

export function useAuthApi() {
	return {
		login: (data: { userName: string; password: string }) =>
			request<{ code: number; message: string; data: LoginResult }>({ url: '/auth/login', method: 'post', data }),
		me: () => request<{ code: number; message: string; data: Record<string, any> }>({ url: '/auth/me', method: 'get' }),
		logout: () => request({ url: '/auth/logout', method: 'post' }),
	};
}
