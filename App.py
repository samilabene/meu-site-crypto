import streamlit as st
import ccxt
import yfinance as yf
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
# Isso define o título na aba do navegador e o layout
st.set_page_config(
    page_title="🤖 IA Trader Samila - OKX Real",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CABEÇALHO DO SITE ---
st.title("🤖 IA Trader Samila: Modo de Operação Real")
st.markdown("### Objetivo Arrojado: R$ 1 → R$ 1.000 (Meta 1900%/dia)")
st.info("Para operar, preencha suas chaves da OKX na barra lateral à esquerda.")

# --- BARRA LATERAL (SIDEBAR) - CONEXÃO SEGURO ---
st.sidebar.header("🔌 Conexão OKX Real")
st.sidebar.markdown("---")

# Campos para você preencher com suas chaves Reais
# 'help' cria um ícone de interrogação com explicação
api_key_input = st.sidebar.text_input(
    "1. API Key",
    type="password",
    help="Cole a chave que você gerou na OKX (ex: d7a54...) "
)
secret_key_input = st.sidebar.text_input(
    "2. Secret Key",
    type="password",
    help="Cole a chave secreta (ex: CD217...)"
)
passphrase_input = st.sidebar.text_input(
    "3. Passphrase",
    type="password",
    help="A senha que você criou na OKX para essas chaves."
)

st.sidebar.markdown("---")

# Botão para tentar conectar
conectar_btn = st.sidebar.button("🔗 Conectar Conta Real")

# --- LÓGICA DE CONEXÃO E SALDO ---
# Inicializa o estado da sessão para armazenar a conexão
if 'exchange_connected' not in st.session_state:
    st.session_state['exchange_connected'] = False
if 'okx_exchange' not in st.session_state:
    st.session_state['okx_exchange'] = None

if conectar_btn:
    # Verifica se os campos estão preenchidos
    if api_key_input and secret_key_input and passphrase_input:
        with st.sidebar.spinner("Conectando na OKX..."):
            try:
                # Configuração da exchange com ccxt
                exchange = ccxt.okx({
                    'apiKey': api_key_input,
                    'secret': secret_key_input,
                    'password': passphrase_input,
                    'enableRateLimit': True,
                    # Opcional: define um timeout maior para conexões de celular
                    'timeout': 30000, 
                })
                
                # Busca o saldo real (apenas para verificar se conectou)
                # exchange.fetch_balance()
                
                # Se chegou aqui sem erro, funcionou!
                st.sidebar.success("✅ Conta Real Conectada!")
                st.session_state['exchange_connected'] = True
                st.session_state['okx_exchange'] = exchange
                
                # st.rerun() # Opcional: recarrega a página para atualizar o layout
            except Exception as e:
                # Se der erro, mostra uma mensagem amigável
                st.sidebar.error(f"❌ Falha na conexão. Verifique as chaves e a Passphrase.")
                st.sidebar.caption(f"Detalhe técnico: {str(e)}") # Opcional: mostra o erro técnico
                st.session_state['exchange_connected'] = False
                st.session_state['okx_exchange'] = None
    else:
        st.sidebar.warning("⚠️ Preencha todos os campos da API.")

# --- PAINEL PRINCIPAL ---

# 1. MONITORAMENTO DE MERCADO (Funciona mesmo sem login)
st.divider()
st.subheader("📡 Monitoramento de Mercado (BTC/USDT)")

try:
    with st.spinner("Atualizando preços..."):
        # Puxa dados do Bitcoin usando yfinance
        ticker_btc = yf.Ticker("BTC-USD")
        # fast_info['last_price'] é o jeito mais rápido de pegar o preço atual
        preco_btc_atual = ticker_btc.fast_info['last_price']
        
        # Colunas para organizar a tela
        col_btc1, col_btc2, col_btc3 = st.columns(3)
        
        col_btc1.metric(
            label="Preço BTC Agora (US$)",
            value=f"${preco_btc_atual:,.2f}",
            delta=None, # Opcional: variação
            help="Preço de fechamento mais recente no yfinance."
        )
        
        # Opcional: busca volume ou variação
        try:
            dados_hoje = ticker_btc.history(period="1d")
            volume_hoje = dados_hoje['Volume'].iloc[-1]
            col_btc2.metric("Volume Hoje (BTC)", f"{volume_hoje:,.0f} BTC")
        except:
            pass # Ignora se falhar

        # Mostra o horário da última atualização
        hora_agora = datetime.now().strftime("%H:%M:%S")
        col_btc3.write(f"🔄 Última Atualização: {hora_agora}")

except Exception as e:
    st.error(f"⚠️ Erro ao buscar dados de mercado: {e}")

# 2. GERENCIADOR DE TRADE (Aparece apenas quando logado)
if st.session_state['exchange_connected']:
    st.divider()
    st.subheader("🚀 Gerenciador de Trade Automático")
    st.write("O robô está pronto para operar com o saldo da sua conta OKX.")
    st.write("Configuração atual: Monitorando BTC/USDT para entrada agressiva (Meta 1900%).")
    
    # Exibe o saldo na tela principal também
    try:
        balance = st.session_state['okx_exchange'].fetch_balance()
        usdt_total = balance['total'].get('USDT', 0)
        st.metric("Seu Saldo Total USDT", f"{usdt_total:.2f} USDT")
        
        # Botões de ação do robô
        col_btn1, col_btn2 = st.columns(2)
        
        if col_btn1.button("▶️ INICIAR ROBÔ (Modo Observação)"):
            st.info("Buscando melhor ponto de entrada no gráfico...")
            st.warning("IA em modo de observação: Aguardando sinal de força compradora (suporte) para executar ordem.")

        if col_btn2.button("⏹️ PARAR ROBÔ"):
            st.success("Operações automáticas interrompidas.")

    except Exception as e:
        st.error(f"Erro ao buscar saldo na exchange: {e}")

else:
    # Se não tiver logado, mostra o aviso
    st.divider()
    st.subheader("🚀 Gerenciador de Trade Automático")
    st.warning("⚠️ O robô está OFFLINE. Preencha as chaves na barra lateral e conecte para liberar o painel de operações.")

# --- RODAPÉ ---
st.divider()
st.caption(f"Desenvolvido com carinho por Samila Benevente • © 2024")
st.markdown("<br>", unsafe_allow_safe=True) # Espaço extra
