export interface LocalMenu {
	id: number;
	pid: number | null;
	path: string;
	name: string;
	component: string;
	redirect?: string;
	menuType: 'menu' | 'btn';
	menuSort: number;
	btnPower?: string;
	meta: {
		title: string;
		icon: string;
		isHide: boolean;
		isKeepAlive: boolean;
		isAffix: boolean;
		isLink: string;
		isIframe: boolean;
		roles: string[];
	};
}

export interface LocalUnit { id: number; deptName: string; deptShortName: string; expireTime: string }
export interface LocalRole { id: number; roleName: string; dataScope: string; code: string; menuPaths: string[]; btnPermissions: string[] }
export interface LocalUser { id: number; userName: string; realName: string; phone: string; status: boolean; unitId: number | null; roleIds: number[] }
