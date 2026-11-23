using System;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class HUD_ChatBox : Singleton<HUD_ChatBox>
{
	public struct MsgMaskRectData
	{
		public float time;

		public float height;

		public MsgMaskRectData(float time, float height)
		{
			this.time = 0f;
			this.height = 0f;
		}
	}

	public enum Channel
	{
		All = 0,
		Teammate = 1,
		Clan = 2
	}

	[SerializeField]
	private InputField inputField;

	[SerializeField]
	private RectTransform msgMask;

	private float tempMsgMaskHeight;

	[SerializeField]
	private Text msgText;

	[SerializeField]
	private Text tempMsgText;

	private bool firstMsg;

	private Queue<MsgMaskRectData> maskDataQueue;

	public static readonly string color_JoinGame;

	public static readonly string color_ExitGame;

	public static readonly string color_Radio;

	public static readonly string color_System;

	public static readonly string color_Normal;

	public static readonly string color_Teammate;

	public static readonly string color_VIP;

	private string[] gameTip;

	private Dictionary<string, Action> simpleCommand;

	protected override void Awake()
	{
	}

	private void PlayerController_FocusHUD_Listenner(ref string hud)
	{
	}

	private void Update()
	{
	}

	public void AddSimpleMsg(string color, string msg)
	{
	}

	private void MsgMaskHeightUpdate()
	{
	}

	private void MsgMaskHeightSetting()
	{
	}

	private void OnPlayerJoinGame(Player newPlayer)
	{
	}

	private void OnPlayerInputText(string text)
	{
	}

	public override void SetVisible(bool visible)
	{
	}

	private void TryGetWpnCommand(int wpnIndex)
	{
	}

	private void TryBecomeGhostBlade()
	{
	}

	private void TryBecomeArmoredTerminator()
	{
	}

	private void TryBecomeMasterHero()
	{
	}

	private void GameTip()
	{
	}
}
