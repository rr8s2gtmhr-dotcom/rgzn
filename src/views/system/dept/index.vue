<template>
	<div class="system-dept-container layout-padding">
		<div class="system-dept-padding layout-padding-view layout-padding-auto">
			<div class="system-dept-actions mb15">
				<el-button type="success" @click="onAdd">新增单位</el-button>
			</div>
			<Table
				ref="tableRef"
				:data="state.tableData.data"
				:header="state.tableData.header"
				:config="state.tableData.config"
				class="system-dept-table"
				@delRow="onDelRow"
				@editRow="onEditRow"
				@pageChange="onPageChange"
				@sortHeader="onSortHeader"
			/>
			<CrudDialog v-model="state.dialogVisible" :title="state.dialogTitle" :fields="state.fields" :initial="state.editing" @submit="onDialogSubmit" />
		</div>
	</div>
</template>

<script setup lang="ts" name="systemDept">
import { defineAsyncComponent, reactive, ref, onMounted } from 'vue';
import { useBusinessCrud } from '/@/utils/businessCrud';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const CrudDialog = defineAsyncComponent(() => import('/@/components/crudDialog/index.vue'));

const crud = useBusinessCrud('units');
const tableRef = ref<RefType>();
const state = reactive<BusinessTableState & { dialogVisible: boolean; dialogTitle: string; editing: EmptyObjectType; fields: CrudField[] }>({
	dialogVisible: false,
	dialogTitle: '',
	editing: {},
	fields: [
		{ key: 'deptName', label: '部门名称', required: true },
		{ key: 'deptShortName', label: '部门简称' },
		{ key: 'expireTime', label: '到期时间', type: 'date' },
	],
	tableData: {
		data: [],
		header: [
			{ key: 'deptName', colWidth: '', title: '部门名称', type: 'text', width: '', isCheck: true },
			{ key: 'deptShortName', colWidth: '', title: '部门简称', type: 'text', width: '', isCheck: true },
			{ key: 'expireTime', colWidth: '160', title: '到期时间', type: 'text', width: '', isCheck: true },
		],
		config: {
			total: 0,
			loading: false,
			isBorder: false,
			isSelection: false,
			isSerialNo: false,
			isOperate: true,
			isEdit: true,
			disableDeleteConfirm: true,
			enableHeaderColumnSetting: true,
		},
		search: [],
		param: { pageNum: 1, pageSize: 10 },
	},
});

const getTableData = async () => {
	state.tableData.loading = true;
	try {
		const { rows, total } = await crud.page(state.tableData.param);
		state.tableData.data = rows;
		state.tableData.config.total = total;
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
	state.dialogTitle = '新增单位';
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogTitle = '修改单位';
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	getTableData();
};
const onDelRow = async (row: EmptyObjectType) => {
	try {
		await crud.remove(row, `单位 ${row.deptName}`);
		getTableData();
	} catch {
		// 用户取消删除
	}
};

onMounted(getTableData);
</script>

<style scoped lang="scss">
.system-dept-container {
	.system-dept-padding {
		padding: 15px;
	}
	.system-dept-table {
		flex: 1;
		overflow: hidden;
	}
}
</style>
