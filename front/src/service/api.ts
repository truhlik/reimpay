/** Generate by swagger-axios-codegen */
// tslint:disable
/* eslint-disable */
import axiosStatic, { AxiosInstance } from 'axios';

export interface IRequestOptions {
  headers?: any;
  baseURL?: string;
  responseType?: string;
}

interface IRequestConfig {
  method?: any;
  headers?: any;
  url?: any;
  data?: any;
  params?: any;
}

// Add options interface
export interface ServiceOptions {
  axios?: AxiosInstance;
}

// Add default options
export const serviceOptions: ServiceOptions = {};

// Instance selector
function axios(configs: IRequestConfig, resolve: (p: any) => void, reject: (p: any) => void): Promise<any> {
  if (serviceOptions.axios) {
    return serviceOptions.axios
      .request(configs)
      .then(res => {
        resolve(res.data);
      })
      .catch(err => {
        reject(err);
      });
  } else {
    throw new Error('please inject yourself instance like axios  ');
  }
}

function getConfigs(method: string, contentType: string, url: string, options: any): IRequestConfig {
  const configs: IRequestConfig = { ...options, method, url };
  configs.headers = {
    ...options.headers,
    'Content-Type': contentType
  };
  return configs;
}

export class IList<T> extends Array<T> {}
export class List<T> extends Array<T> {}

export interface IListResult<T> {
  items?: T[];
}

export class ListResultDto<T> implements IListResult<T> {
  items?: T[];
}

export interface IPagedResult<T> extends IListResult<T> {
  totalCount: number;
}

export class PagedResultDto<T> implements IPagedResult<T> {
  totalCount!: number;
}

// customer definition
// empty

export class AccountsService {
  /**
   *
   */
  static accountsLoginCreate(
    params: {
      /**  */
      data: Login;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Login> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/login/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Calls Django logout method and delete the Token object
assigned to the current User object.
 */
  static accountsLogoutList(options: IRequestOptions = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/logout/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Calls Django logout method and delete the Token object
assigned to the current User object.
 */
  static accountsLogoutCreate(options: IRequestOptions = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/logout/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   * Calls Django Auth SetPasswordForm save method.
   */
  static accountsPasswordChangeCreate(
    params: {
      /**  */
      data: PasswordChange;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PasswordChange> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/password/change/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   * Calls Django Auth PasswordResetForm save method.
   */
  static accountsPasswordResetCreate(
    params: {
      /**  */
      data: CustomPasswordReset;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<CustomPasswordReset> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/password/reset/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Password reset e-mail link is confirmed, therefore
this resets the user's password.
 */
  static accountsPasswordResetConfirmCreate(
    params: {
      /**  */
      data: PasswordResetConfirm;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PasswordResetConfirm> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/password/reset/confirm/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.
 */
  static accountsUserRead(options: IRequestOptions = {}): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/user/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.
 */
  static accountsUserUpdate(
    params: {
      /**  */
      data: User;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/user/';

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
 * Reads and updates UserModel fields
Accepts GET, PUT, PATCH methods.
 */
  static accountsUserPartialUpdate(
    params: {
      /**  */
      data: User;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/accounts/user/';

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class AddressesService {
  /**
   *
   */
  static addressesSuggestionCreate(
    params: {
      /**  */
      data: AddressSuggestion;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<AddressResponse> {
    return new Promise((resolve, reject) => {
      let url = '/addresses/suggestion/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class AresService {
  /**
   *
   */
  static aresCompanyList(options: IRequestOptions = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/ares/company/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class ArmsService {
  /**
   *
   */
  static armsList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/arms/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { study_id: params['studyId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static armsCreate(
    params: {
      /**  */
      data: Arm;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Arm> {
    return new Promise((resolve, reject) => {
      let url = '/arms/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static armsRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Arm> {
    return new Promise((resolve, reject) => {
      let url = '/arms/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static armsUpdate(
    params: {
      /**  */
      data: Arm;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Arm> {
    return new Promise((resolve, reject) => {
      let url = '/arms/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static armsPartialUpdate(
    params: {
      /**  */
      data: Arm;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Arm> {
    return new Promise((resolve, reject) => {
      let url = '/arms/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static armsDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/arms/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class CompaniesService {
  /**
   *
   */
  static companiesList(
    params: {
      /** A search term. */
      q?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/companies/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { q: params['q'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static companiesPrimaryRead(
    params: {
      /** A search term. */
      q?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/companies/primary/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { q: params['q'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static companiesPrimaryUpdate(
    params: {
      /**  */
      data: BaseCompany;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<BaseCompany> {
    return new Promise((resolve, reject) => {
      let url = '/companies/primary/';

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static companiesPrimaryPartialUpdate(
    params: {
      /**  */
      data: BaseCompany;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<BaseCompany> {
    return new Promise((resolve, reject) => {
      let url = '/companies/primary/';

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static companiesRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<BaseCompany> {
    return new Promise((resolve, reject) => {
      let url = '/companies/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class CreditService {
  /**
   *
   */
  static creditList(
    params: {
      /**  */
      createdAtDateLte?: string;
      /**  */
      createdAtDateGte?: string;
      /**  */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/credit/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        created_at__date__lte: params['createdAtDateLte'],
        created_at__date__gte: params['createdAtDateGte'],
        study_id: params['studyId'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static creditExport(
    params: {
      /**  */
      createdAtDateLte?: string;
      /**  */
      createdAtDateGte?: string;
      /**  */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/credit/export/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        created_at__date__lte: params['createdAtDateLte'],
        created_at__date__gte: params['createdAtDateGte'],
        study_id: params['studyId'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static creditRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<CreditBalance> {
    return new Promise((resolve, reject) => {
      let url = '/credit/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class DoctorService {
  /**
   *
   */
  static doctorLoginCreate(options: IRequestOptions = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/doctor/login/';

      const configs: IRequestConfig = getConfigs('post', 'multipart/form-data', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class FinanceService {
  /**
   *
   */
  static financeRead(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<CreditInfo> {
    return new Promise((resolve, reject) => {
      let url = '/finance/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static financeStats(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyStat> {
    return new Promise((resolve, reject) => {
      let url = '/finance/{id}/stats/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class HistoryService {
  /**
   *
   */
  static historyList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/history/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { study_id: params['studyId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class InvoicesService {
  /**
   *
   */
  static invoicesList(
    params: {
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/invoices/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static invoicesRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Invoice> {
    return new Promise((resolve, reject) => {
      let url = '/invoices/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class PatientVisitItemsService {
  /**
   *
   */
  static patientVisitItemsList(
    params: {
      /** Dummy help text */
      approved?: string;
      /** Dummy help text */
      studyId?: string;
      /** Dummy help text */
      patientVisitPatientSiteId?: number;
      /** Dummy help text */
      patientVisitPatientId?: number;
      /** Dummy help text */
      paymentStatus?: string;
      /** Dummy help text */
      patientVisit?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visit-items/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        approved: params['approved'],
        study_id: params['studyId'],
        patient_visit__patient__site__id: params['patientVisitPatientSiteId'],
        patient_visit__patient__id: params['patientVisitPatientId'],
        payment_status: params['paymentStatus'],
        patient_visit: params['patientVisit'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientVisitItemsCreate(
    params: {
      /**  */
      data: PatientVisitItem;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientVisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visit-items/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientVisitItemsUpdate(
    params: {
      /**  */
      data: PatientVisitItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientVisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientVisitItemsPartialUpdate(
    params: {
      /**  */
      data: PatientVisitItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientVisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class PatientVisitsService {
  /**
   *
   */
  static patientVisitsList(
    params: {
      /** Dummy help text */
      patientId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visits/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { patient_id: params['patientId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientVisitsCreate(
    params: {
      /**  */
      data: PatientVisit;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientVisit> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visits/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientVisitsDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/patient-visits/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class PatientsService {
  /**
   *
   */
  static patientsList(
    params: {
      /** Dummy help text */
      active?: string;
      /** Dummy help text */
      studyId?: string;
      /** Dummy help text */
      siteId?: number;
      /** Dummy help text */
      changePayment?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/patients/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        active: params['active'],
        study_id: params['studyId'],
        site_id: params['siteId'],
        change_payment: params['changePayment'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientsCreate(
    params: {
      /**  */
      data: PatientBase;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientBase> {
    return new Promise((resolve, reject) => {
      let url = '/patients/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientsRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientDetail> {
    return new Promise((resolve, reject) => {
      let url = '/patients/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientsUpdate(
    params: {
      /**  */
      data: PatientBase;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientBase> {
    return new Promise((resolve, reject) => {
      let url = '/patients/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static patientsPartialUpdate(
    params: {
      /**  */
      data: PatientBase;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<PatientBase> {
    return new Promise((resolve, reject) => {
      let url = '/patients/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class SitesService {
  /**
   *
   */
  static sitesList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** Dummy help text */
      id?: number;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/sites/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        study_id: params['studyId'],
        id: params['id'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesCreate(
    params: {
      /**  */
      data: Site;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Site> {
    return new Promise((resolve, reject) => {
      let url = '/sites/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesPatients(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** Dummy help text */
      id?: number;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/sites/patients/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        study_id: params['studyId'],
        id: params['id'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Site> {
    return new Promise((resolve, reject) => {
      let url = '/sites/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesUpdate(
    params: {
      /**  */
      data: Site;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Site> {
    return new Promise((resolve, reject) => {
      let url = '/sites/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesPartialUpdate(
    params: {
      /**  */
      data: Site;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Site> {
    return new Promise((resolve, reject) => {
      let url = '/sites/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static sitesDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/sites/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class StudiesService {
  /**
   *
   */
  static studiesList(
    params: {
      /** Dummy help text */
      id?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/studies/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { id: params['id'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesCreate(
    params: {
      /**  */
      data: StudyWrite;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyWrite> {
    return new Promise((resolve, reject) => {
      let url = '/studies/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesRead(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyRead> {
    return new Promise((resolve, reject) => {
      let url = '/studies/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesUpdate(
    params: {
      /**  */
      data: StudyWrite;
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyWrite> {
    return new Promise((resolve, reject) => {
      let url = '/studies/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesPartialUpdate(
    params: {
      /**  */
      data: StudyWrite;
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyWrite> {
    return new Promise((resolve, reject) => {
      let url = '/studies/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesDelete(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/studies/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studiesConfig(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyConfig> {
    return new Promise((resolve, reject) => {
      let url = '/studies/{id}/config/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class StudyItemsService {
  /**
   *
   */
  static studyItemsList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { study_id: params['studyId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studyItemsCreate(
    params: {
      /**  */
      data: StudyItem;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyItem> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studyItemsRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyItem> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studyItemsUpdate(
    params: {
      /**  */
      data: StudyItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyItem> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studyItemsPartialUpdate(
    params: {
      /**  */
      data: StudyItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<StudyItem> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static studyItemsDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/study-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class TicketsService {
  /**
   *
   */
  static ticketsCreate(
    params: {
      /**  */
      data: Ticket;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Ticket> {
    return new Promise((resolve, reject) => {
      let url = '/tickets/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class TopupsService {
  /**
   *
   */
  static topupsList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/topups/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { study_id: params['studyId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static topupsCreate(
    params: {
      /**  */
      data: TopUp;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<TopUp> {
    return new Promise((resolve, reject) => {
      let url = '/topups/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class UsersService {
  /**
   *
   */
  static usersList(
    params: {
      /** Dummy help text */
      role?: string;
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/users/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        role: params['role'],
        study_id: params['studyId'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersCreate(
    params: {
      /**  */
      data: User;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/users/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersSelfRead(
    params: {
      /** Dummy help text */
      role?: string;
      /** Dummy help text */
      studyId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/users/self/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        role: params['role'],
        study_id: params['studyId'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersSelfPartialUpdate(
    params: {
      /**  */
      data: User;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/users/self/';

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersSelfDelete(options: IRequestOptions = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/users/self/';

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersRead(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/users/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersUpdate(
    params: {
      /**  */
      data: User;
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/users/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersPartialUpdate(
    params: {
      /**  */
      data: User;
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<User> {
    return new Promise((resolve, reject) => {
      let url = '/users/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static usersDelete(
    params: {
      /**  */
      id: string;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/users/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class VisitItemsService {
  /**
   *
   */
  static visitItemsList(
    params: {
      /** Dummy help text */
      visitId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = { visit_id: params['visitId'], page: params['page'], page_size: params['pageSize'] };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitItemsCreate(
    params: {
      /**  */
      data: VisitItem;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<VisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitItemsRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<VisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitItemsUpdate(
    params: {
      /**  */
      data: VisitItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<VisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitItemsPartialUpdate(
    params: {
      /**  */
      data: VisitItem;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<VisitItem> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitItemsDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/visit-items/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class VisitsService {
  /**
   *
   */
  static visitsList(
    params: {
      /** Dummy help text */
      studyId?: string;
      /** Dummy help text */
      armId?: string;
      /** A page number within the paginated result set. */
      page?: number;
      /** Number of results to return per page. */
      pageSize?: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/visits/';

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);
      configs.params = {
        study_id: params['studyId'],
        arm_id: params['armId'],
        page: params['page'],
        page_size: params['pageSize']
      };
      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitsCreate(
    params: {
      /**  */
      data: Visit;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Visit> {
    return new Promise((resolve, reject) => {
      let url = '/visits/';

      const configs: IRequestConfig = getConfigs('post', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitsRead(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Visit> {
    return new Promise((resolve, reject) => {
      let url = '/visits/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('get', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitsUpdate(
    params: {
      /**  */
      data: Visit;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Visit> {
    return new Promise((resolve, reject) => {
      let url = '/visits/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('put', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitsPartialUpdate(
    params: {
      /**  */
      data: Visit;
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<Visit> {
    return new Promise((resolve, reject) => {
      let url = '/visits/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('patch', 'application/json', url, options);

      let data = params['data'];

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
  /**
   *
   */
  static visitsDelete(
    params: {
      /**  */
      id: number;
    } = {} as any,
    options: IRequestOptions = {}
  ): Promise<any> {
    return new Promise((resolve, reject) => {
      let url = '/visits/{id}/';
      url = url.replace('{id}', params['id'] + '');

      const configs: IRequestConfig = getConfigs('delete', 'application/json', url, options);

      let data = null;

      configs.data = data;
      axios(configs, resolve, reject);
    });
  }
}

export class Login {
  /**  */
  'username': string;

  /**  */
  'email': string;

  /**  */
  'password': string;

  constructor(data: undefined | any = {}) {
    this['username'] = data['username'];
    this['email'] = data['email'];
    this['password'] = data['password'];
  }
}

export class PasswordChange {
  /**  */
  'new_password1': string;

  /**  */
  'new_password2': string;

  constructor(data: undefined | any = {}) {
    this['new_password1'] = data['new_password1'];
    this['new_password2'] = data['new_password2'];
  }
}

export class CustomPasswordReset {
  /**  */
  'email': string;

  constructor(data: undefined | any = {}) {
    this['email'] = data['email'];
  }
}

export class PasswordResetConfirm {
  /**  */
  'new_password1': string;

  /**  */
  'new_password2': string;

  /**  */
  'uid': string;

  /**  */
  'token': string;

  constructor(data: undefined | any = {}) {
    this['new_password1'] = data['new_password1'];
    this['new_password2'] = data['new_password2'];
    this['uid'] = data['uid'];
    this['token'] = data['token'];
  }
}

export class User {
  /**  */
  'id': string;

  /**  */
  'role': EnumUserRole;

  /**  */
  'first_name': string;

  /**  */
  'last_name': string;

  /**  */
  'email': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['role'] = data['role'];
    this['first_name'] = data['first_name'];
    this['last_name'] = data['last_name'];
    this['email'] = data['email'];
  }
}

export class AddressSuggestion {
  /**  */
  'city': string;

  /**  */
  'street': string;

  /**  */
  'number': string;

  /**  */
  'post_code': string;

  /**  */
  'suggesting_field': string;

  constructor(data: undefined | any = {}) {
    this['city'] = data['city'];
    this['street'] = data['street'];
    this['number'] = data['number'];
    this['post_code'] = data['post_code'];
    this['suggesting_field'] = data['suggesting_field'];
  }
}

export class AddressResponse {
  /**  */
  'results': AddressSuggestion[];

  constructor(data: undefined | any = {}) {
    this['results'] = data['results'];
  }
}

export class Arm {
  /**  */
  'id': number;

  /**  */
  'title': string;

  /**  */
  'study': string;

  /**  */
  'max_unscheduled': number;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['title'] = data['title'];
    this['study'] = data['study'];
    this['max_unscheduled'] = data['max_unscheduled'];
  }
}

export class BaseCompany {
  /**  */
  'id': number;

  /**  */
  'name': string;

  /**  */
  'image': string;

  /**  */
  'description': string;

  /**  */
  'email': string;

  /**  */
  'phone': string;

  /**  */
  'web': string;

  /**  */
  'reg_number': string;

  /**  */
  'vat_number': string;

  /**  */
  'street': string;

  /**  */
  'street_number': string;

  /**  */
  'city': string;

  /**  */
  'zip': string;

  /**  */
  'address': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['name'] = data['name'];
    this['image'] = data['image'];
    this['description'] = data['description'];
    this['email'] = data['email'];
    this['phone'] = data['phone'];
    this['web'] = data['web'];
    this['reg_number'] = data['reg_number'];
    this['vat_number'] = data['vat_number'];
    this['street'] = data['street'];
    this['street_number'] = data['street_number'];
    this['city'] = data['city'];
    this['zip'] = data['zip'];
    this['address'] = data['address'];
  }
}

export class CreditBalance {
  /**  */
  'id': number;

  /**  */
  'balance_type': EnumCreditBalanceBalanceType;

  /**  */
  'balance_amount': string;

  /**  */
  'created_at': Date;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['balance_type'] = data['balance_type'];
    this['balance_amount'] = data['balance_amount'];
    this['created_at'] = data['created_at'];
  }
}

export class CreditInfo {
  /**  */
  'actual_balance': string;

  /**  */
  'paid': string;

  /**  */
  'max_cost': string;

  /**  */
  'remaining_visits': number;

  /**  */
  'avg_visit_value': string;

  /**  */
  'exp_budget_need': string;

  constructor(data: undefined | any = {}) {
    this['actual_balance'] = data['actual_balance'];
    this['paid'] = data['paid'];
    this['max_cost'] = data['max_cost'];
    this['remaining_visits'] = data['remaining_visits'];
    this['avg_visit_value'] = data['avg_visit_value'];
    this['exp_budget_need'] = data['exp_budget_need'];
  }
}

export class StudyStat {
  /**  */
  'stats': string;

  constructor(data: undefined | any = {}) {
    this['stats'] = data['stats'];
  }
}

export class AuditLog {
  /**  */
  'user': string;

  /**  */
  'created_at': Date;

  /**  */
  'content_type': string;

  /**  */
  'update_data': object;

  /**  */
  'action': string;

  /**  */
  'obj_name': string;

  constructor(data: undefined | any = {}) {
    this['user'] = data['user'];
    this['created_at'] = data['created_at'];
    this['content_type'] = data['content_type'];
    this['update_data'] = data['update_data'];
    this['action'] = data['action'];
    this['obj_name'] = data['obj_name'];
  }
}

export class Invoice {
  /**  */
  'id': number;

  /**  */
  'company': number;

  /**  */
  'fakturoid_public_url': string;

  /**  */
  'invoice_number': string;

  /**  */
  'issue_date': Date;

  /**  */
  'amount': number;

  /**  */
  'status': EnumInvoiceStatus;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['company'] = data['company'];
    this['fakturoid_public_url'] = data['fakturoid_public_url'];
    this['invoice_number'] = data['invoice_number'];
    this['issue_date'] = data['issue_date'];
    this['amount'] = data['amount'];
    this['status'] = data['status'];
  }
}

export class StudyItem {
  /**  */
  'id': number;

  /**  */
  'title': string;

  /**  */
  'description': string;

  /**  */
  'price': number;

  /**  */
  'study': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['title'] = data['title'];
    this['description'] = data['description'];
    this['price'] = data['price'];
    this['study'] = data['study'];
  }
}

export class BaseVisit {
  /**  */
  'id': number;

  /**  */
  'arm': number;

  /**  */
  'name': string;

  /**  */
  'title': string;

  /**  */
  'number': number;

  /**  */
  'visit_type': string;

  /**  */
  'order': number;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['arm'] = data['arm'];
    this['name'] = data['name'];
    this['title'] = data['title'];
    this['number'] = data['number'];
    this['visit_type'] = data['visit_type'];
    this['order'] = data['order'];
  }
}

export class VisitItem {
  /**  */
  'id': number;

  /**  */
  'visit': number;

  /**  */
  'study_item': number;

  /**  */
  'study_item_obj': StudyItem;

  /**  */
  'visit_obj': BaseVisit;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['visit'] = data['visit'];
    this['study_item'] = data['study_item'];
    this['study_item_obj'] = data['study_item_obj'];
    this['visit_obj'] = data['visit_obj'];
  }
}

export class Site {
  /**  */
  'id': number;

  /**  */
  'title': string;

  /**  */
  'study': string;

  /**  */
  'expected_patients': number;

  /**  */
  'cra': string;

  /**  */
  'cra_obj': User;

  /**  */
  'contract_path': string;

  /**  */
  'site_instructions_path': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['title'] = data['title'];
    this['study'] = data['study'];
    this['expected_patients'] = data['expected_patients'];
    this['cra'] = data['cra'];
    this['cra_obj'] = data['cra_obj'];
    this['contract_path'] = data['contract_path'];
    this['site_instructions_path'] = data['site_instructions_path'];
  }
}

export class PatientBase {
  /**  */
  'id': number;

  /**  */
  'arm': number;

  /**  */
  'number': string;

  /**  */
  'payment_type': EnumPatientBasePaymentType;

  /**  */
  'payment_info': string;

  /**  */
  'arm_name': string;

  /**  */
  'visits': number;

  /**  */
  'paid': number;

  /**  */
  'site': number;

  /**  */
  'name': string;

  /**  */
  'street': string;

  /**  */
  'street_number': string;

  /**  */
  'city': string;

  /**  */
  'zip': string;

  /**  */
  'site_obj': Site;

  /**  */
  'change_payment_request': boolean;

  /**  */
  'status': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['arm'] = data['arm'];
    this['number'] = data['number'];
    this['payment_type'] = data['payment_type'];
    this['payment_info'] = data['payment_info'];
    this['arm_name'] = data['arm_name'];
    this['visits'] = data['visits'];
    this['paid'] = data['paid'];
    this['site'] = data['site'];
    this['name'] = data['name'];
    this['street'] = data['street'];
    this['street_number'] = data['street_number'];
    this['city'] = data['city'];
    this['zip'] = data['zip'];
    this['site_obj'] = data['site_obj'];
    this['change_payment_request'] = data['change_payment_request'];
    this['status'] = data['status'];
  }
}

export class PatientVisitItem {
  /**  */
  'id': number;

  /**  */
  'visit_item': number;

  /**  */
  'patient_visit': string;

  /**  */
  'visit_item_obj': VisitItem;

  /**  */
  'patient_obj': PatientBase;

  /**  */
  'date': Date;

  /**  */
  'approved': boolean;

  /**  */
  'status': string;

  /**  */
  'origin': string;

  /**  */
  'reject_reason': string;

  /**  */
  'flagged': string;

  /**  */
  'can_be_deleted': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['visit_item'] = data['visit_item'];
    this['patient_visit'] = data['patient_visit'];
    this['visit_item_obj'] = data['visit_item_obj'];
    this['patient_obj'] = data['patient_obj'];
    this['date'] = data['date'];
    this['approved'] = data['approved'];
    this['status'] = data['status'];
    this['origin'] = data['origin'];
    this['reject_reason'] = data['reject_reason'];
    this['flagged'] = data['flagged'];
    this['can_be_deleted'] = data['can_be_deleted'];
  }
}

export class PatientVisit {
  /**  */
  'id': string;

  /**  */
  'patient': number;

  /**  */
  'visit_type': EnumPatientVisitVisitType;

  /**  */
  'visit_date': Date;

  /**  */
  'visit_items': number[];

  /**  */
  'visit': number;

  /**  */
  'title': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['patient'] = data['patient'];
    this['visit_type'] = data['visit_type'];
    this['visit_date'] = data['visit_date'];
    this['visit_items'] = data['visit_items'];
    this['visit'] = data['visit'];
    this['title'] = data['title'];
  }
}

export class Visit {
  /**  */
  'id': number;

  /**  */
  'arm': number;

  /**  */
  'name': string;

  /**  */
  'title': string;

  /**  */
  'number': number;

  /**  */
  'visit_type': string;

  /**  */
  'visit_items': VisitItem[];

  /**  */
  'order': number;

  /**  */
  'visit_items_cost': number;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['arm'] = data['arm'];
    this['name'] = data['name'];
    this['title'] = data['title'];
    this['number'] = data['number'];
    this['visit_type'] = data['visit_type'];
    this['visit_items'] = data['visit_items'];
    this['order'] = data['order'];
    this['visit_items_cost'] = data['visit_items_cost'];
  }
}

export class BaseStudy {
  /**  */
  'id': string;

  /**  */
  'status': EnumBaseStudyStatus;

  /**  */
  'number': string;

  /**  */
  'identifier': string;

  /**  */
  'notes': string;

  /**  */
  'bank_transfer': boolean;

  /**  */
  'post_office_cash': boolean;

  /**  */
  'pay_frequency': number;

  /**  */
  'operator': EnumBaseStudyOperator;

  /**  */
  'sponsor_name': string;

  /**  */
  'bank_account': string;

  /**  */
  'active_patients': string;

  /**  */
  'paid': string;

  /**  */
  'credit': string;

  /**  */
  'date_launched': Date;

  /**  */
  'date_last_visit': Date;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['status'] = data['status'];
    this['number'] = data['number'];
    this['identifier'] = data['identifier'];
    this['notes'] = data['notes'];
    this['bank_transfer'] = data['bank_transfer'];
    this['post_office_cash'] = data['post_office_cash'];
    this['pay_frequency'] = data['pay_frequency'];
    this['operator'] = data['operator'];
    this['sponsor_name'] = data['sponsor_name'];
    this['bank_account'] = data['bank_account'];
    this['active_patients'] = data['active_patients'];
    this['paid'] = data['paid'];
    this['credit'] = data['credit'];
    this['date_launched'] = data['date_launched'];
    this['date_last_visit'] = data['date_last_visit'];
  }
}

export class PatientVisitItemNormalized {
  /**  */
  'payment': number;

  /**  */
  'visit': string;

  /**  */
  'date': Date;

  /**  */
  'amount': number;

  /**  */
  'note': string;

  /**  */
  'payment_status': EnumPatientVisitItemNormalizedPaymentStatus;

  /**  */
  'reject_reason': string;

  constructor(data: undefined | any = {}) {
    this['payment'] = data['payment'];
    this['visit'] = data['visit'];
    this['date'] = data['date'];
    this['amount'] = data['amount'];
    this['note'] = data['note'];
    this['payment_status'] = data['payment_status'];
    this['reject_reason'] = data['reject_reason'];
  }
}

export class PatientDetail {
  /**  */
  'id': number;

  /**  */
  'arm': number;

  /**  */
  'number': string;

  /**  */
  'payment_type': EnumPatientDetailPaymentType;

  /**  */
  'payment_info': string;

  /**  */
  'arm_name': string;

  /**  */
  'visits': number;

  /**  */
  'paid': number;

  /**  */
  'site': number;

  /**  */
  'next_visits': Visit[];

  /**  */
  'study_obj': BaseStudy;

  /**  */
  'patient_visit_items': PatientVisitItemNormalized[];

  /**  */
  'unscheduled_left': string;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['arm'] = data['arm'];
    this['number'] = data['number'];
    this['payment_type'] = data['payment_type'];
    this['payment_info'] = data['payment_info'];
    this['arm_name'] = data['arm_name'];
    this['visits'] = data['visits'];
    this['paid'] = data['paid'];
    this['site'] = data['site'];
    this['next_visits'] = data['next_visits'];
    this['study_obj'] = data['study_obj'];
    this['patient_visit_items'] = data['patient_visit_items'];
    this['unscheduled_left'] = data['unscheduled_left'];
  }
}

export class SitePatient {
  /**  */
  'patients': PatientBase[];

  /**  */
  'id': number;

  /**  */
  'title': string;

  /**  */
  'study': string;

  /**  */
  'expected_patients': number;

  /**  */
  'cra': string;

  /**  */
  'contract_path': string;

  /**  */
  'site_instructions_path': string;

  constructor(data: undefined | any = {}) {
    this['patients'] = data['patients'];
    this['id'] = data['id'];
    this['title'] = data['title'];
    this['study'] = data['study'];
    this['expected_patients'] = data['expected_patients'];
    this['cra'] = data['cra'];
    this['contract_path'] = data['contract_path'];
    this['site_instructions_path'] = data['site_instructions_path'];
  }
}

export class StudyRead {
  /**  */
  'id': string;

  /**  */
  'status': EnumStudyReadStatus;

  /**  */
  'number': string;

  /**  */
  'identifier': string;

  /**  */
  'notes': string;

  /**  */
  'bank_transfer': boolean;

  /**  */
  'post_office_cash': boolean;

  /**  */
  'pay_frequency': number;

  /**  */
  'operator': EnumStudyReadOperator;

  /**  */
  'sponsor_name': string;

  /**  */
  'bank_account': string;

  /**  */
  'active_patients': string;

  /**  */
  'paid': string;

  /**  */
  'credit': string;

  /**  */
  'date_launched': Date;

  /**  */
  'date_last_visit': Date;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['status'] = data['status'];
    this['number'] = data['number'];
    this['identifier'] = data['identifier'];
    this['notes'] = data['notes'];
    this['bank_transfer'] = data['bank_transfer'];
    this['post_office_cash'] = data['post_office_cash'];
    this['pay_frequency'] = data['pay_frequency'];
    this['operator'] = data['operator'];
    this['sponsor_name'] = data['sponsor_name'];
    this['bank_account'] = data['bank_account'];
    this['active_patients'] = data['active_patients'];
    this['paid'] = data['paid'];
    this['credit'] = data['credit'];
    this['date_launched'] = data['date_launched'];
    this['date_last_visit'] = data['date_last_visit'];
  }
}

export class StudyWrite {
  /**  */
  'id': string;

  /**  */
  'status': EnumStudyWriteStatus;

  /**  */
  'number': string;

  /**  */
  'identifier': string;

  /**  */
  'notes': string;

  /**  */
  'bank_transfer': boolean;

  /**  */
  'post_office_cash': boolean;

  /**  */
  'pay_frequency': number;

  /**  */
  'operator': EnumStudyWriteOperator;

  /**  */
  'sponsor_name': string;

  /**  */
  'bank_account': string;

  /**  */
  'active_patients': string;

  /**  */
  'paid': string;

  /**  */
  'credit': string;

  /**  */
  'date_launched': Date;

  /**  */
  'date_last_visit': Date;

  constructor(data: undefined | any = {}) {
    this['id'] = data['id'];
    this['status'] = data['status'];
    this['number'] = data['number'];
    this['identifier'] = data['identifier'];
    this['notes'] = data['notes'];
    this['bank_transfer'] = data['bank_transfer'];
    this['post_office_cash'] = data['post_office_cash'];
    this['pay_frequency'] = data['pay_frequency'];
    this['operator'] = data['operator'];
    this['sponsor_name'] = data['sponsor_name'];
    this['bank_account'] = data['bank_account'];
    this['active_patients'] = data['active_patients'];
    this['paid'] = data['paid'];
    this['credit'] = data['credit'];
    this['date_launched'] = data['date_launched'];
    this['date_last_visit'] = data['date_last_visit'];
  }
}

export class StudyConfig {
  /**  */
  'config': string;

  constructor(data: undefined | any = {}) {
    this['config'] = data['config'];
  }
}

export class Ticket {
  /**  */
  'subject': string;

  /**  */
  'text': string;

  constructor(data: undefined | any = {}) {
    this['subject'] = data['subject'];
    this['text'] = data['text'];
  }
}

export class TopUp {
  /**  */
  'created_at': Date;

  /**  */
  'study': string;

  /**  */
  'amount': number;

  /**  */
  'file': string;

  constructor(data: undefined | any = {}) {
    this['created_at'] = data['created_at'];
    this['study'] = data['study'];
    this['amount'] = data['amount'];
    this['file'] = data['file'];
  }
}
export enum EnumUserRole {
  'ADMIN' = 'ADMIN',
  'CRA' = 'CRA'
}
export enum EnumCreditBalanceBalanceType {
  'TOPUP' = 'TOPUP',
  'COMMISSION' = 'COMMISSION',
  'PATIENT_PAYCHECK' = 'PATIENT_PAYCHECK',
  'BANK_TRANSFER_FEE' = 'BANK_TRANSFER_FEE',
  'POST_OFFICE_FEE' = 'POST_OFFICE_FEE',
  'TOPDOWN' = 'TOPDOWN'
}
export enum EnumInvoiceStatus {
  'ISSUED' = 'ISSUED',
  'PAID' = 'PAID',
  'CANCELLED' = 'CANCELLED'
}
export enum EnumPatientBasePaymentType {
  'BANK' = 'BANK',
  'POST' = 'POST'
}
export enum EnumPatientVisitVisitType {
  'UNSCHEDULED' = 'UNSCHEDULED',
  'DISCONTINUAL' = 'DISCONTINUAL',
  'REGULAR' = 'REGULAR'
}
export enum EnumBaseStudyStatus {
  'DRAFT' = 'DRAFT',
  'PRELAUNCH' = 'PRELAUNCH',
  'PROGRESS' = 'PROGRESS',
  'BILLING' = 'BILLING',
  'CLOSED' = 'CLOSED'
}
export enum EnumBaseStudyOperator {
  'CRO' = 'CRO',
  'SPONSOR' = 'SPONSOR'
}
export enum EnumPatientVisitItemNormalizedPaymentStatus {
  'WAITING' = 'WAITING',
  'SENT' = 'SENT',
  'RETURNED' = 'RETURNED'
}
export enum EnumPatientDetailPaymentType {
  'BANK' = 'BANK',
  'POST' = 'POST'
}
export enum EnumStudyReadStatus {
  'DRAFT' = 'DRAFT',
  'PRELAUNCH' = 'PRELAUNCH',
  'PROGRESS' = 'PROGRESS',
  'BILLING' = 'BILLING',
  'CLOSED' = 'CLOSED'
}
export enum EnumStudyReadOperator {
  'CRO' = 'CRO',
  'SPONSOR' = 'SPONSOR'
}
export enum EnumStudyWriteStatus {
  'DRAFT' = 'DRAFT',
  'PRELAUNCH' = 'PRELAUNCH',
  'PROGRESS' = 'PROGRESS',
  'BILLING' = 'BILLING',
  'CLOSED' = 'CLOSED'
}
export enum EnumStudyWriteOperator {
  'CRO' = 'CRO',
  'SPONSOR' = 'SPONSOR'
}
