<template>
	<div class="system-role-container layout-padding">
		<div class="system-role-padding layout-padding-view layout-padding-auto">
			<div class="system-role-actions mb15">
				<el-button type="success" @click="onAdd">新增角色</el-button>
			</div>
			<Table
				ref="tableRef"
				:data="state.tableData.data"
				:header="state.tableData.header"
				:config="state.tableData.config"
				class="system-role-table"
				@delRow="onDelRow"
				@editRow="onEditRow"
				@pageChange="onPageChange"
				@sortHeader="onSortHeader"
			/>
			<RoleDialog v-model="state.dialogVisible" :initial="state.editing" :menus="state.menus" @submit="onDialogSubmit" />
		</div>
	</div>
</template>

<script setup lang="ts" name="systemRole">
import { defineAsyncComponent, reactive, ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useBusinessCrud } from '/@/utils/businessCrud';
import { refreshFrontEndRoutes } from '/@/router/frontEnd';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const RoleDialog = defineAsyncComponent(() => import('/@/views/system/role/dialog.vue'));

const crud = useBusinessCrud('roles');
const tableRef = ref<RefType>();
const state = reactive<BusinessTableState & { dialogVisible: boolean; editing: EmptyObjectType; menus: EmptyObjectType[] }>({
	dialogVisible: false,
	editing: {},
	menus: [],
	tableData: {
		data: [],
		header: [
			{ key: 'roleName', colWidth: '', title: '角色名称', type: 'text', width: '', isCheck: true },
			{ key: 'dataScope', colWidth: '', title: '数据范围', type: 'text', width: '', isCheck: true },
		],
		config: {
			total: 0,
			loading: false,
			isBorder: false,
			isSelection: false,
			isSerialNo: true,
			isOperate: true,
			isEdit: true,
			disableDeleteConfirm: true,
		},
		search: [],
		param: { pageNum: 1, pageSize: 10 },
	},
});

const getTableData = async () => {
	state.tableData.loading = true;
	try {
		const [{ rows, total }, menus] = await Promise.all([crud.page(state.tableData.param), crud.api.list('menus')]);
		state.tableData.data = rows;
		state.tableData.config.total = total;
		state.menus = (menus.data as any[]) || [];
	} finally {
		state.tableData.loading = false;
	}
};
const onPageChange = (page: TableDemoPageType) => {
	state.tableData.param.pageNum = page.pageNum;
	state.tableData.param.pageSize = page.pageSize;
};
const onSortHeader = (data: TableHeaderType[]) => {
	state.tableData.header = data;
};
const onAdd = () => {
	state.editing = {};
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	await refreshFrontEndRoutes();
	getTableData();
};
const onDelRow = async (row: EmptyObjectType) => {
	if (row.code === 'admin') {
		ElMessage.warning('管理员角色不可删除');
		return;
	}
	try {
		await crud.remove(row, `角色 ${row.roleName}`);
		await refreshFrontEndRoutes();
		getTableData();
	} catch {
		// 用户取消删除
	}
};

onMounted(getTableData);
</script>

<style scoped lang="scss">
.system-role-container {
	.system-role-padding {
		padding: 15px;
	}
	.system-role-table {
		flex: 1;
		overflow: hidden;
	}
}
</style>
