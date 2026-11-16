import { ElMessage, ElMessageBox } from 'element-plus';
import { useResourceApi, type ResourceKey, type PageQuery } from '/@/api/resource';

/**
 * 业务页面通用 CRUD 逻辑（数据来自后端 API）
 */
export function useBusinessCrud(resource: ResourceKey, options: { deleteLabel?: (row: any) => string } = {}) {
	const api = useResourceApi();

	const page = async (params: PageQuery) => {
		const res = await api.page(resource, params);
		const data = res.data as { list: any[]; total: number };
		return { rows: data.list || [], total: data.total || 0 };
	};

	const list = async () => {
		const res = await api.list(resource);
		return (res.data as any[]) || [];
	};

	const submit = async (form: any) => {
		if (form.id) await api.update(resource, form.id, form);
		else await api.create(resource, form);
		ElMessage.success(form.id ? '修改成功' : '新增成功');
	};

	const remove = async (row: any, label?: string) => {
		const text = label || (row.deviceNo || row.name || row.id);
		await ElMessageBox.confirm(`确定删除 ${text} 吗？`, '提示', { type: 'warning' });
		await api.remove(resource, row.id);
		ElMessage.success('删除成功');
	};

	return { api, page, list, submit, remove };
}
