import { defineStore } from 'pinia';

/**
 * 权限辅助（数据来自后端登录接口返回的用户信息）
 */
export const useRbac = defineStore('rbac', {
	actions: {
		hasRole(roles: string[], userRoles: string[]) {
			return roles.some((role) => userRoles.includes(role));
		},
		hasBtn(btn: string, authBtnList: string[]) {
			return authBtnList.includes(btn);
		},
	},
});
