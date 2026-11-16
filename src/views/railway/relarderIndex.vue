<template>
	<div class="railway-page layout-padding">
		<div class="railway-page-content layout-padding-view layout-padding-auto">
			<TableSearch :search="state.tableData.search" @search="onSearch">
				<template #actions>
					<el-button type="success" @click="onAdd">新增设备</el-button>
				</template>
			</TableSearch>
			<Table
				ref="tableRef"
				:data="state.tableData.data"
				:header="state.tableData.header"
				:config="state.tableData.config"
				class="railway-table"
				@delRow="onDelRow"
				@editRow="onEditRow"
				@pageChange="onPageChange"
				@sortHeader="onSortHeader"
			/>
			<CrudDialog v-model="state.dialogVisible" :title="state.dialogTitle" :fields="state.fields" :initial="state.editing" @submit="onDialogSubmit" />
		</div>
	</div>
</template>

<script setup lang="ts" name="railwayRelarder">
import { defineAsyncComponent, reactive, ref, onMounted } from 'vue';
import { useBusinessCrud } from '/@/utils/businessCrud';

const Table = defineAsyncComponent(() => import('/@/components/table/index.vue'));
const TableSearch = defineAsyncComponent(() => import('/@/components/tableSearch/index.vue'));
const CrudDialog = defineAsyncComponent(() => import('/@/components/crudDialog/index.vue'));

const crud = useBusinessCrud('relarders');
const tableRef = ref<RefType>();
const state = reactive<BusinessTableState & { dialogVisible: boolean; dialogTitle: string; editing: EmptyObjectType; fields: CrudField[] }>({
	dialogVisible: false,
	dialogTitle: '',
	editing: {},
	fields: [
		{ key: 'deviceNo', label: '设备编号', required: true },
		{ key: 'factory', label: '厂家' },
		{ key: 'model', label: '规格型号' },
		{ key: 'address', label: '安装地点' },
		{ key: 'trackNo', label: '股道号' },
		{ key: 'enableTime', label: '启用时间', type: 'date' },
		{ key: 'damageTime', label: '报损时间', type: 'date' },
		{ key: 'remark', label: '备注', type: 'textarea' },
	],
	tableData: {
		data: [],
		header: [
			{ key: 'deviceNo', colWidth: '140', title: '设备编号', type: 'text', width: '', isCheck: true },
			{ key: 'factory', colWidth: '', title: '厂家', type: 'text', width: '', isCheck: true },
			{ key: 'model', colWidth: '', title: '规格型号', type: 'text', width: '', isCheck: true },
			{ key: 'address', colWidth: '', title: '安装地点', type: 'text', width: '', isCheck: true },
			{ key: 'trackNo', colWidth: '', title: '股道号', type: 'text', width: '', isCheck: true },
			{ key: 'enableTime', colWidth: '160', title: '启用时间', type: 'text', width: '', isCheck: true },
			{ key: 'damageTime', colWidth: '160', title: '报损时间', type: 'text', width: '', isCheck: true },
			{ key: 'remark', colWidth: '', title: '备注', type: 'text', width: '', isCheck: false },
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
			enableHeaderColumnSetting: true,
		},
		search: [
			{ label: '编号', prop: 'deviceNo', placeholder: '请输入编号', required: false, type: 'input' },
			{ label: '站段', prop: 'trackNo', placeholder: '请输入股道', required: false, type: 'input' },
		],
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
const onSearch = (data: EmptyObjectType) => {
	state.tableData.param = Object.assign({}, state.tableData.param, data);
	tableRef.value?.pageReset();
	getTableData();
};
const onPageChange = (page: TableDemoPageType) => {
	state.tableData.param.pageNum = page.pageNum;
	state.tableData.param.pageSize = page.pageSize;
	getTableData();
};
const onSortHeader = (data: TableHeaderType[]) => {
	state.tableData.header = data;
};
const onAdd = () => {
	state.editing = {};
	state.dialogTitle = '新增设备';
	state.dialogVisible = true;
};
const onEditRow = (row: EmptyObjectType) => {
	state.editing = { ...row };
	state.dialogTitle = '修改设备';
	state.dialogVisible = true;
};
const onDialogSubmit = async (form: EmptyObjectType) => {
	await crud.submit(form);
	getTableData();
};
const onDelRow = async (row: EmptyObjectType) => {
	try {
		await crud.remove(row, `设备 ${row.deviceNo}`);
		getTableData();
	} catch {
		// 用户取消删除
	}
};

onMounted(getTableData);
</script>

<style scoped lang="scss">
.railway-page {
	.railway-page-content {
		padding: 15px;
	}
	.railway-table {
		flex: 1;
		overflow: hidden;
	}
}
</style>
