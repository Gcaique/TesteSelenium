from selenium.webdriver.common.by import By

FIRST_ACCESS_CREATE_PASSWORD = (By.ID, "select-number") # Utilizado na primeira modal do Primeiro Acesso

SEND_BY_EMAIL = (By.XPATH, "//li[@class='type-send-option']/span[normalize-space()='E-MAIL']") # Utilizado na segunda modal (Validação), onde é selecionado o enivo do token por e-mail

EMAIL_OPTION_2 = (By.XPATH, "(//ul[@class='options-list']//input[@name='email'])[2]") # Utilizado na terceira modal (Selecione), onde é selecionado a segunda opção do e-mail

BTN_SEND_CODE_2 = (By.XPATH, "(//*[@id='resend-code'])[2]") # Utilizado na terceria modal (Selecione) botão Avançar.

TOKEN_INPUT = (By.ID, "token") # Utilizado na quarta modal (Verifique), campo de inserção do token
BTN_VERIFY_TOKEN = (By.ID, "verify-token") # Utilizado na quarta modal (Verifique), botão Avançar

EMAIL_FIRST_ACCESS = (By.ID, "email-first-access") # Utilizado na quinta modal (Criar credenciais), campo de inserção de e-mail
PASSWORD_FIRST_ACCESS = (By.XPATH, "(//*[@name='password'])[1]") # Utilizado na quinta modal (Criar credenciais), campo de inserção da senha
CONFIRM_PASSWORD = (By.NAME, "confirm-password") # Utilizado na quinta modal (Criar credenciais), campo de inserção da cnfirmação de senha

BTN_SAVE_ACCOUNT = (By.ID, "save-account") # Utilizado na quinta modal (Criar credenciais), botão Criar Senha
BTN_SAVE_ACCOUNT_DISABLED = (By.XPATH, "//input[@id='save-account' and @disabled='disabled']") # Utilizado na quinta modal (Criar credenciais), botão Criar Senha desabilitado
BTN_CLOSE_MODAL_LOGIN = (By.ID, "close-modal-login") # Utilizado na ultima modal (Senha criada com sucesso), botão Entrar
