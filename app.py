import streamlit as st
import time
import random

# Configuração da página
st.set_page_config(page_title="Painel Antifraude - Consórcio", page_icon="🛡️", layout="wide")

st.title("🛡️ Painel de Validação e Risco de Faturamento")
st.markdown("Cruze os dados da vistoria, do consorciado e do vendedor para detectar fraudes em faturamentos de veículos.")

# --- MÓDULOS DE UPLOAD E INPUT ---
col1, col2, col3 = st.columns(3)

with col1:
    st.header("1. Vistoria (Infovist)")
    arquivo_vistoria = st.file_uploader("Upload do Laudo (PDF)", type=["pdf"], key="vistoria")
    
    if arquivo_vistoria:
        st.success("Laudo carregado com sucesso!")
        # Simulação de extração de dados do PDF de vistoria
        local_vistoria = "Goiânia - GO"
        score_ia_fotos = random.choice(["Aprovado - Fotos Autênticas", "Alerta DDI - Possível foto de tela!"])
        
        st.write(f"**Local Identificado:** {local_vistoria}")
        if "Alerta" in score_ia_fotos:
            st.error(f"**IA de Imagens:** {score_ia_fotos}")
        else:
            st.success(f"**IA de Imagens:** {score_ia_fotos}")

with col2:
    st.header("2. Consorciado")
    # Referência ao arquivo Consorcio conforme solicitado
    arquivo_consorcio = st.file_uploader("Upload do arquivo Consorcio (PDF)", type=["pdf"], key="consorcio")
    
    if arquivo_consorcio:
        st.success("Parecer de Crédito carregado!")
        # Simulação de extração do documento Consorcio
        cidade_consorciado = "Curitiba - PR"
        saldo_devedor = "R$ 150.000,00"
        parcelas_pagas = "2/80"
        risco_original = "Médio"
        
        st.write(f"**Localidade:** {cidade_consorciado}")
        st.write(f"**Saldo Devedor:** {saldo_devedor} (Pagas: {parcelas_pagas})")
        st.write(f"**Risco na Aprovação:** {risco_original}")

with col3:
    st.header("3. Vendedor")
    doc_vendedor = st.text_input("Digite o CPF ou CNPJ do Vendedor")
    
    if doc_vendedor:
        # Simulação de retorno de API da Receita Federal
        tempo_abertura = random.choice(["2 meses", "5 anos", "10 anos"])
        local_vendedor = "Fortaleza - CE" if len(doc_vendedor) > 11 else "São Paulo - SP"
        
        st.info("Buscando dados na Receita/Birô...")
        time.sleep(1) # Efeito de carregamento
        
        st.write(f"**Tempo de Abertura:** {tempo_abertura}")
        st.write(f"**Localidade (Sede):** {local_vendedor}")
        if tempo_abertura == "2 meses":
            st.warning("Alerta: Empresa recém-aberta.")


# --- MOTOR DE REGRAS (ERP VISUAL) ---
st.divider()
st.header("⚙️ Motor de Risco e Veredito")

if st.button("Gerar Análise de Risco da Operação", type="primary"):
    if not (arquivo_vistoria and arquivo_consorcio and doc_vendedor):
        st.warning("Por favor, preencha as 3 etapas (Vistoria, arquivo Consorcio e Vendedor) antes de analisar.")
    else:
        with st.spinner("Cruzando dados operacionais..."):
            time.sleep(2) # Simula processamento
            
            # Lógica simples do motor de regras (Baseado nos dados simulados acima)
            pontos_risco = 0
            motivos = []
            
            # Regra 1: Triangulação Geográfica
            if cidade_consorciado[-2:] != local_vistoria[-2:]:
                pontos_risco += 2
                motivos.append("Triangulação Suspeita: Consorciado de um estado e Vistoria em outro.")
            
            # Regra 2: Empresa Recente
            if tempo_abertura == "2 meses":
                pontos_risco += 1
                motivos.append("Vendedor de Alto Risco: CNPJ recém-aberto.")
                
            # Regra 3: Alerta da IA nas fotos
            if "Alerta DDI" in score_ia_fotos:
                pontos_risco += 3
                motivos.append("Fraude Visual: IA detectou adulteração ou foto tirada de uma tela nas imagens da vistoria.")
            
            # Regra 4: Risco Financeiro (Poucas parcelas pagas)
            if "2/" in parcelas_pagas:
                pontos_risco += 1
                motivos.append("Risco Financeiro: Consorciado com pouquíssimas parcelas pagas e alto saldo devedor.")

            # Veredito Final
            st.subheader("Veredito:")
            if pontos_risco >= 4:
                st.error("🚨 RISCO ALTO - FATURAMENTO BLOQUEADO")
            elif pontos_risco >= 2:
                st.warning("⚠️ RISCO MÉDIO - REQUER ANÁLISE MANUAL APROFUNDADA")
            else:
                st.success("✅ RISCO BAIXO - OPERAÇÃO LIBERADA")
                
            if motivos:
                st.write("**Gatilhos acionados:**")
                for m in motivos:
                    st.write(f"- {m}")
