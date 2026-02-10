from selenium.webdriver.common.by import By


# ---------------------------
# PÁGINA FAVORITOS (WISHLIST)
# ---------------------------
WISHLIST_TOOLBAR_COUNT = (By.XPATH, "//*[@class='toolbar wishlist-toolbar top']//span")

# Botões de ações (card)
WISHLIST_INCREMENT_BY_INDEX = lambda idx: (By.XPATH, f"(//div[@class='product-item-inner']//button[contains(@class,'increment-qty')])[{idx}]",)
WISHLIST_DECREMENT_BY_INDEX = lambda idx: (By.XPATH, f"(//div[@class='product-item-inner']//button[contains(@class,'decrement-qty')])[{idx}]",)
WISHLIST_QTY_INPUTS = (By.XPATH, "//div[contains(@class,'product-item-inner')]//input[@type='number']",)
WISHLIST_QTY_INPUT_BY_INDEX = lambda idx: (By.XPATH, f"(//div[@class='product-item-inner']//input[@type='number'])[{idx}]",)
WISHLIST_TOCART_BTN_BY_INDEX = lambda idx: (By.XPATH, f"(//button[contains(@class, 'action tocart primary tget-btn-buy tocart')])[{idx}]",) # botões de comprar individuais dentro da lista de favoritos

# Botão de adicionar tudo ao carrinho
WISHLIST_ADD_ALL_TO_CART = (By.XPATH, "//button[@class='action tocart']")

# status "favorito" (algumas telas mudam o title/classe)
WISHLIST_STATUS_FAVORITO = (By.XPATH, "//button[@title='Favorito']")
WISHLIST_STATUS_ADDED_CLASS = (By.XPATH, "//button[@class='action add-to-wishlist hj-product_card-add_to_wishlist onwishlist']")

# AVISE-ME (wishlist)
BTN_AVISE_DISABLED = (By.XPATH, "//a[contains(@id,'button_disabled')]//span[contains(normalize-space(text()),'Avise-me')]")
BTN_AVISE_ENABLED = (By.XPATH, "//a[contains(@id,'button_enabled') and .//span[contains(.,'avis')]]")

# TOGGLE FAVORITO na lista
WISHLIST_REMOVE_ONWISHLIST_BY_INDEX = lambda idx: (By.XPATH, f"(//*[@class='product-photo-wishilist-remove-wrapper']/button[contains(@class,'onwishlist')])[{idx}]",)
WISHLIST_ADD_TOWISHLIST = (By.XPATH, "//*[@class='product-photo-wishilist-remove-wrapper']/button[contains(@class,'towishlist')]")

# REMOVER ITENS
REMOVE_CARD_BTN_BY_INDEX = lambda idx: (By.XPATH, f"(//*[@class='product details product-item-details']//a[@class='btn-remove action delete'])[{idx}]",)
CONFIRM_MODAL_ACCEPT = (By.XPATH, "//button[@class='action-primary action-accept']")

# contador de itens adicionados na lista de favoritos
WISHLIST_TOOLBAR = (By.XPATH, "//*[@class='toolbar wishlist-toolbar top']")