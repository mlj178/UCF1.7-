using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class ModeBase : Singleton<ModeBase>
{
	protected Vector2Int score;

	protected int currentRound;

	public static int targetRound;

	public static int targetScore;

	public static Vector2Int gameTime;

	public static float respawnTime;

	protected bool BLOnLeft;

	private RawImage scoreBoardImage;

	[SerializeField]
	private Texture[] scoreBoardTex;

	private Text scoreText_L;

	private Text scoreText_R;

	private Text roundText_T;

	private Text roundText_C;

	protected Vector2Int restGameTime;

	private Text timeText_M;

	private Text timeText_S;

	[SerializeField]
	private Material timeFlashMat;

	private int playerCountBL;

	private int playerCountGR;

	private int aliveCountBL;

	private int aliveCountGR;

	[SerializeField]
	private GameObject rectContainer;

	[SerializeField]
	private GameObject playerRectPrefab;

	private SimpleObjectPool playerRectPool;

	private List<HUD_PlayerRect> playerRect_BL;

	private List<HUD_PlayerRect> playerRect_GR;

	protected Player myPlayer;

	[SerializeField]
	private string[] modeTip;

	protected bool timeFlash
	{
		set
		{
		}
	}

	public static bool playerRectVisible
	{
		set
		{
		}
	}

	public bool isRoundGame => false;

	protected override void Awake()
	{
	}

	protected virtual void ScoreBoardTexSetting()
	{
	}

	protected virtual void Start()
	{
	}

	protected virtual void Update()
	{
	}

	private void UpdatePlayerRect()
	{
	}

	protected virtual void OnStartNewGameRound()
	{
	}

	public void ResetTime(int minute, int second)
	{
	}

	private IEnumerator RoundTimer()
	{
		return null;
	}

	private void UpdateTimeUI()
	{
	}

	public void SetCurrentRound(int value)
	{
	}

	public void AddCurrentRound()
	{
	}

	public void SetLeftScore(int value)
	{
	}

	public void AddLeftScore()
	{
	}

	public void SetRightScore(int value)
	{
	}

	public void AddRightScore()
	{
	}

	protected virtual void OnScoreReachTarget(bool left)
	{
	}

	protected virtual void OnTimeOut()
	{
	}

	protected virtual void OnMyPlayerJoin(Player myPlayer)
	{
	}

	protected virtual void ShowModeTip()
	{
	}

	protected void ExitGame(float delay)
	{
	}

	protected void RefreshNextRound(float waitTime)
	{
	}
}
