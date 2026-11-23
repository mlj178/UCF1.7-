using UnityEngine;
using UnityEngine.UI;

public class HUD_Nano4T_Attribute : MonoBehaviour
{
	[SerializeField]
	private GameObject timerTipBG;

	[SerializeField]
	private HUD_Nano4T_AttributeIcon nanoIcon;

	[SerializeField]
	private HUD_Nano4T_AttributeIcon humanIcon;

	[SerializeField]
	private Image header;

	[SerializeField]
	private Sprite[] headerSpr;

	[SerializeField]
	private Text timer;

	[SerializeField]
	private Image nanoImg;

	private Text nanoLayer;

	[SerializeField]
	private Image humanImg;

	private Text humanLayer;

	private bool isNanoBuffMax10;

	[SerializeField]
	private Image battleIcon;

	[SerializeField]
	private Image battleAttributeImg;

	private Text battleAttributeText;

	[SerializeField]
	private Sprite[] battleAttributeSprs;

	[SerializeField]
	private GameObject battleCDBg;

	private Text battleCDText;

	private void Awake()
	{
	}

	private void GameManager_MyPlayerJoinEvent_Observers(Player myPlayer)
	{
	}

	private void NanoRole_listener(NanoRole oldRole, NanoRole newRole)
	{
	}

	public void NewRoundReset(Nano4T_Attribute nanoAtt, Nano4T_Attribute humanAtt)
	{
	}

	public void StartBattleCountDown()
	{
	}

	public void StartNanoTimerCountDown()
	{
	}

	public void OnNanoGhostAppear()
	{
	}

	private void UpdateNanoLayer(int arg1, int newLayer)
	{
	}

	private void UpdateHumanLayer(int arg1, int newLayer)
	{
	}

	private void UpdateLayer(Text text, int layer, bool max10)
	{
	}
}
